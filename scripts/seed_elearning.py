"""Provision synthetic users/data only in demo-minicloud local emulators."""
import json
import secrets
from datetime import datetime, timezone
import requests
from lab import ROOT, config

PROJECT = "demo-minicloud"
AUTH = "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:"
DOCS = "http://127.0.0.1:8180/v1/projects/" + PROJECT + "/databases/(default)/documents/"

def credentials():
    cfg = config()
    for key in ("ELEARNING_INSTRUCTOR_PASSWORD", "ELEARNING_STUDENT_PASSWORD"):
        if not cfg.get(key):
            cfg[key] = secrets.token_urlsafe(20)
            with (ROOT / ".env").open("a", encoding="utf-8") as file:
                file.write("\n" + key + "=" + cfg[key] + "\n")
    return cfg

def encode(value):
    if isinstance(value, bool): return {"booleanValue": value}
    if isinstance(value, int): return {"integerValue": str(value)}
    if isinstance(value, dict): return {"mapValue": {"fields": {k: encode(v) for k, v in value.items()}}}
    return {"stringValue": str(value)}

def document(path, data):
    response = requests.patch(DOCS + path, headers={"Authorization": "Bearer owner"},
        json={"fields": {key: encode(value) for key, value in data.items()}}, timeout=20)
    response.raise_for_status()
    return response.json()

def sign_in(email, password):
    response = requests.post(AUTH + "signInWithPassword?key=demo-key", json={
        "email": email, "password": password, "returnSecureToken": True}, timeout=20)
    response.raise_for_status()
    return response.json()

def seed():
    cfg = credentials()
    users = {}
    now = datetime.now(timezone.utc).isoformat()
    for role, name in (("instructor", "Demo Instructor"), ("student", "Demo Student")):
        email = role + "@example.test"
        password = cfg["ELEARNING_" + role.upper() + "_PASSWORD"]
        response = requests.post(AUTH + "signUp?key=demo-key", json={
            "email": email, "password": password, "returnSecureToken": True}, timeout=20)
        if response.status_code != 200:
            assert response.json().get("error", {}).get("message") == "EMAIL_EXISTS", response.status_code
        user = sign_in(email, password)
        users[role] = user["localId"]
        document("users/" + user["localId"], {"uid": user["localId"], "email": email,
            "username": role, "name": name, "displayName": name, "role": role,
            "isActive": True, "createdAtLocal": now, "settings": {"status": "active", "language": "vi", "theme": "light"}})
    course = {"code": "CLOUD101", "name": "Cloud Computing Lab", "instructor": users["instructor"],
        "teacherName": "Demo Instructor", "semester": "HK1_2026", "sessions": 12,
        "description": "Synthetic course for MyMiniCloud demo", "status": "active", "imageUrl": ""}
    # Preserve user edits to the demo course across subsequent checks.
    response = requests.get(DOCS + "course_of_study/minicloud101", headers={"Authorization": "Bearer owner"}, timeout=20)
    if response.status_code == 404: document("course_of_study/minicloud101", course)
    else: response.raise_for_status()
    document("semesters/HK1_2026", {"id": "HK1_2026", "code": "HK1_2026", "name": "HK1_2026",
        "startDate": "2026-09-01T00:00:00", "endDate": "2027-01-31T00:00:00", "isActive": True, "createdAt": now})
    document("groups/minicloud-group", {"name": "Lab Group A", "courseId": "minicloud101",
        "instructor": users["instructor"], "code": "LAB-A", "status": "active"})
    document("enrollments/minicloud101_" + users["student"], {"courseId": "minicloud101",
        "userId": users["student"], "studentName": "Demo Student", "studentEmail": "student@example.test",
        "enrolledAt": now, "role": "student", "status": "active", "groupId": "minicloud-group"})
    return users

if __name__ == "__main__":
    seed()
    print("Seeded synthetic E-learning users, course, semester and enrollment in local demo emulators.")
