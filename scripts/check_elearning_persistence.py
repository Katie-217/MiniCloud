"""Verify emulator read/write and retained users/course/object across recreation."""
import hashlib
import requests
from lab import run, save, result
from seed_elearning import seed, credentials, sign_in, DOCS, encode

users = seed()
cfg = credentials()
user = sign_in("instructor@example.test", cfg["ELEARNING_INSTRUCTOR_PASSWORD"])
headers = {"Authorization": "Bearer " + user["idToken"]}
target = DOCS + "demo_checks/persistence-marker"
response = requests.patch(target, headers=headers, json={"fields": {
    "message": encode("MyMiniCloud E-learning persistent data"), "verified": encode(True)}}, timeout=15)
response.raise_for_status()
expected = response.json()["fields"]
course_list = requests.get(DOCS + "course_of_study", headers={"Authorization": "Bearer owner"}, timeout=15)
course_list.raise_for_status()
courses_before = {doc["name"]: doc["fields"] for doc in course_list.json().get("documents", [])}
storage = "http://127.0.0.1:9199/v0/b/demo-minicloud.appspot.com/o"
payload = b"MyMiniCloud synthetic E-learning storage persistence check\n"
response = requests.post(storage, params={"uploadType": "media", "name": "demo/persistence-note.txt"},
    headers={**headers, "Content-Type": "text/plain"}, data=payload, timeout=15)
response.raise_for_status()

def read_object(token):
    response = requests.get(storage + "/demo%2Fpersistence-note.txt", params={"alt": "media"},
        headers={"Authorization": "Bearer " + token}, timeout=15)
    response.raise_for_status()
    return response.content

assert read_object(user["idToken"]) == payload
before = run("docker", "inspect", "firebase-emulator-server", "--format", "{{.Id}}")
run("docker", "compose", "exec", "-T", "firebase-emulator-server", "firebase", "emulators:export",
    "/data/export", "--force", "--project", "demo-minicloud")
run("docker", "compose", "up", "-d", "--no-deps", "--force-recreate", "--wait", "--wait-timeout", "180",
    "firebase-emulator-server")
after = run("docker", "inspect", "firebase-emulator-server", "--format", "{{.Id}}")
assert before != after
for role in ("instructor", "student"):
    restored = sign_in(role + "@example.test", cfg["ELEARNING_" + role.upper() + "_PASSWORD"])
    assert restored["localId"] == users[role], "Auth user changed after recreation"
restored = sign_in("instructor@example.test", cfg["ELEARNING_INSTRUCTOR_PASSWORD"])
response = requests.get(target, headers={"Authorization": "Bearer " + restored["idToken"]}, timeout=15)
response.raise_for_status()
assert response.json()["fields"] == expected
assert read_object(restored["idToken"]) == payload
course = requests.get(DOCS + "course_of_study/minicloud101", headers={"Authorization": "Bearer owner"}, timeout=15)
course.raise_for_status()
course_list = requests.get(DOCS + "course_of_study", headers={"Authorization": "Bearer owner"}, timeout=15)
course_list.raise_for_status()
courses_after = {doc["name"]: doc["fields"] for doc in course_list.json().get("documents", [])}
assert all(courses_after.get(name) == fields for name, fields in courses_before.items())
path = save("elearning-persistence.json", result("E-learning persistence", {
    "container_recreated": True, "both_auth_uids_preserved": True, "firestore_marker_preserved": True,
    "course_preserved": True, "all_course_documents_preserved": len(courses_before), "storage_bytes_preserved": True,
    "object_sha256": hashlib.sha256(payload).hexdigest(), "export_volume": "firebase-data",
    "credentials": "omitted", "production_firebase_used": False,
}))
print("PASS E-learning persistence: both users, course, Firestore marker and Storage object survived recreation. " + path)
