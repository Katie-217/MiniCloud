from playwright.sync_api import sync_playwright
from browser import launch
from lab import EVIDENCE, save, result
from progress import set_status

details=[]
with sync_playwright() as p:
    browser=launch(p)
    page=browser.new_page(viewport={"width":1100,"height":850})
    for base in ("http://localhost:8080", "http://localhost"):
        response=page.goto(base+"/blog/")
        assert response.status == 200
        for n in range(1,4):
            assert page.locator(f'a[href="/blog/blog{n}.html"]').count()==1
        for n in range(1,4):
            response=page.goto(base+f"/blog/blog{n}.html")
            assert response.status==200
            page.locator("img").wait_for()
            assert page.locator("img").evaluate("el => el.complete && el.naturalWidth > 0")
            assert page.locator('a[href="/"]').count()>=1
            if base=="http://localhost":page.screenshot(path=str(EVIDENCE/f"E01-blog{n}.png"),full_page=True)
            details.append({"url":page.url,"status":response.status,"image_loaded":True,"home_link":True})
    browser.close()
path=save("E01-blog.json",result("E01",details))
set_status("E01","DAT",path+"; feat/personal-blog; python scripts/check_blog.py; E01-blog1/2/3.png")
print("PASS E01: three articles, images and return links on direct/proxy Web.")
