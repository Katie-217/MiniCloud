"""Verify synthetic E-learning data/auth and isolated Flutter browser flows."""
import json
import re
from urllib.parse import urlsplit
import requests
from playwright.sync_api import sync_playwright
from browser import launch
from lab import ROOT, EVIDENCE, save, result
from seed_elearning import seed, credentials, sign_in, DOCS

users = seed()
print("E-learning: synthetic seed ready.", flush=True)
cfg = credentials()
checks = []
for role in ("instructor", "student"):
    user = sign_in(role + "@example.test", cfg["ELEARNING_" + role.upper() + "_PASSWORD"])
    assert user["localId"] == users[role]
    checks.append({"case": role + "_authentication", "passed": True})
response = requests.get(DOCS + "course_of_study/minicloud101", headers={"Authorization": "Bearer owner"}, timeout=15)
response.raise_for_status()
assert response.json()["fields"]["name"]["stringValue"]
checks.append({"case": "seeded_course_read", "passed": True})

blocked = []
browser_errors = []
network = []
with sync_playwright() as p:
    browser = launch(p)
    for role in ("instructor", "student"):
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        def route_request(route):
            host = urlsplit(route.request.url).hostname or ""
            if host.endswith(("googleapis.com", "firebaseio.com", "firebaseapp.com", "firebasestorage.app", "cloudfunctions.net")) and host != "fonts.googleapis.com":
                blocked.append(host)
                print("E-learning: blocked external data host " + host + urlsplit(route.request.url).path, flush=True)
                route.abort()
            else:
                route.continue_()
        context.route("**/*", route_request)
        page = context.new_page()
        page.on("pageerror", lambda error: browser_errors.append(str(error)[:500]))
        page.on("response", lambda response: network.append({"path": urlsplit(response.url).path,
            "host": urlsplit(response.url).hostname, "status": response.status}))
        response = page.goto("http://localhost/elearning/")
        assert response.status == 200
        page.wait_for_selector("flt-semantics-placeholder", state="attached", timeout=60000)
        page.evaluate("document.querySelector('flt-semantics-placeholder')?.click()")
        page.get_by_role("textbox").first.wait_for(timeout=30000)
        for index, value in enumerate((role + "@example.test", cfg["ELEARNING_" + role.upper() + "_PASSWORD"])):
            page.get_by_role("textbox").nth(index).click()
            page.wait_for_timeout(200)
            page.keyboard.press("Control+A")
            page.keyboard.type(value, delay=25)
        page.get_by_role("button", name="Login", exact=True).click()
        print("E-learning: submitted " + role + " browser login.", flush=True)
        try:
            page.get_by_role("button", name="Login", exact=True).wait_for(state="hidden", timeout=45000)
        except Exception:
            page.screenshot(path=str(EVIDENCE / "elearning-login-failure.png"))
            print(page.locator("body").inner_text()[:1400])
            raise
        marker = "Teacher Dashboard" if role == "instructor" else "Hello Demo Student"
        page.get_by_text(marker, exact=True).first.wait_for(timeout=45000)
        page.wait_for_timeout(3000)
        assert page.get_by_role("button", name="Login", exact=True).count() == 0, "Login did not reach dashboard"
        page.screenshot(path=str(EVIDENCE / ("elearning-" + role + ".png")), full_page=True)
        checks.append({"case": role + "_browser_login", "passed": True, "url": page.url})
        section = "Teaching" if role == "instructor" else "Courses"
        page.get_by_text(section, exact=True).first.click()
        try:
            course_label = (page.get_by_label(re.compile("Cloud Computing Lab")) if role == "instructor"
                else page.get_by_text("Cloud Computing Lab", exact=False))
            course_label.first.wait_for(timeout=30000)
        except Exception:
            page.screenshot(path=str(EVIDENCE / "elearning-course-failure.png"))
            print(json.dumps(page.locator("body").inner_text()[:1800], ensure_ascii=True))
            raise
        page.wait_for_function("""() => document.body.innerText.includes('Students: 1') ||
            [...document.querySelectorAll('[aria-label]')].some(el => el.getAttribute('aria-label').includes('Students: 1'))""", timeout=30000)
        checks.append({"case": role + "_live_enrollment_count", "passed": True, "seed_course_students": 1})
        page.screenshot(path=str(EVIDENCE / ("elearning-" + role + "-courses.png")), full_page=True)
        checks.append({"case": role + "_course_from_firestore", "passed": True})
        if role == "instructor":
            listing = requests.get(DOCS + "course_of_study", headers={"Authorization": "Bearer owner"}, timeout=15)
            listing.raise_for_status()
            created = any(doc.get("fields", {}).get("code", {}).get("stringValue") == "DEMOUI29"
                for doc in listing.json().get("documents", []))
            if not created:
                page.get_by_role("button", name="Create Course", exact=True).first.click()
                for label, value in (("Course Code", "DEMOUI29"), ("Course Name", "MiniCloud UI Demo Course"),
                    ("Description", "Created through the imported Flutter interface"), ("Number of Sessions", "12")):
                    field = page.get_by_role("textbox", name=re.compile(label)).first
                    field.click()
                    page.wait_for_timeout(150)
                    page.keyboard.press("Control+A")
                    page.keyboard.type(value, delay=15)
                page.get_by_role("textbox", name=re.compile("Semester")).first.click()
                page.wait_for_timeout(250)
                page.keyboard.press("ArrowDown")
                page.keyboard.press("Enter")
                page.get_by_role("button", name="Create Course", exact=True).last.click()
                page.get_by_role("button", name="OK", exact=True).wait_for(timeout=30000)
                page.screenshot(path=str(EVIDENCE / "elearning-created-course.png"), full_page=True)
                page.get_by_role("button", name="OK", exact=True).click()
            page.get_by_label(re.compile("MiniCloud UI Demo Course")).first.wait_for(timeout=30000)
            checks.append({"case": "course_created_through_ui_and_listed", "passed": True, "code": "DEMOUI29",
                "created_in_this_run": not created, "reused_previous_ui_fixture": created})
        page.reload()
        page.wait_for_function("document.querySelector('flt-semantics-placeholder') || document.querySelector('flt-semantics')", timeout=60000)
        page.evaluate("document.querySelector('flt-semantics-placeholder')?.click()")
        page.get_by_text(marker, exact=True).first.wait_for(timeout=45000)
        assert page.get_by_role("button", name="Login", exact=True).count() == 0
        checks.append({"case": role + "_session_after_refresh", "passed": True})
        context.close()
    browser.close()
assert not blocked, ("Application attempted an external data endpoint", sorted(set(blocked)))
assert not browser_errors, browser_errors
path = save("elearning-demo.json", result("E-learning integration", {
    "source_commit": "9e9ebd539c7f08092ea6855c9aceafe645bd28e0", "url": "http://localhost/elearning/",
    "project": "demo-minicloud", "checks": checks, "blocked_production_hosts": blocked,
    "browser_errors": browser_errors, "responses": network, "credentials": "omitted",
    "scope": "Synthetic local data, course UI creation and enrollment counts; optional external link preview / Google Sign-In not verified",
}))
print("PASS E-learning: two real emulator logins, dashboards, session refresh; no production Firebase requests. " + path)
