"""Exercise the human-facing protected API demo without displaying tokens."""
from playwright.sync_api import sync_playwright
from browser import launch
from lab import EVIDENCE, config, result, save

cfg = config()
checks = []
with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    page.goto("http://localhost/#secure-demo")
    for username in ("sv01", "sv02"):
        page.get_by_label("Tài khoản Keycloak").select_option(username)
        page.get_by_label("Mật khẩu Keycloak").fill(cfg["KEYCLOAK_TEST_PASSWORD"])
        with page.expect_response(lambda response: response.url.endswith("/api/secure")) as response:
            page.get_by_role("button", name="Gọi API có bảo vệ", exact=True).click()
        assert response.value.status == 200
        page.wait_for_function("document.querySelector('#secureResult').textContent.includes('Secure resource OK')")
        assert username in page.locator("#secureResult").inner_text()
        assert page.get_by_label("Mật khẩu Keycloak").input_value() == ""
        assert "access_token" not in page.locator("#secureResult").inner_text()
        checks.append({"case": username, "status": 200, "password_cleared": True})
    page.locator("#secure-demo").screenshot(path=str(EVIDENCE / "portal-secure-success.png"))
    with page.expect_response(lambda response: response.url.endswith("/api/secure")) as response:
        page.get_by_role("button", name="Gọi không có token", exact=True).click()
    assert response.value.status == 401
    page.wait_for_function("document.querySelector('#secureResult').textContent.includes('HTTP 401')")
    page.locator("#secure-demo").screenshot(path=str(EVIDENCE / "portal-secure-missing-token.png"))
    checks.append({"case": "missing_token", "status": 401})
    browser.close()
save("portal-secure-demo.json", result("Protected API UI", {"checks": checks, "secrets": "omitted"}))
print("PASS protected API UI: sv01/sv02 return 200; anonymous returns 401; passwords/tokens not displayed.")
