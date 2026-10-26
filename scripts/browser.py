"""Use Playwright's installed Chromium, including an existing desktop cache."""
import os
from pathlib import Path

def launch(playwright):
    expected = Path(playwright.chromium.executable_path)
    if expected.exists():
        return playwright.chromium.launch(headless=True)
    cache = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
    candidates = sorted(cache.glob("chromium-*/chrome-win64/chrome.exe"), reverse=True)
    if candidates:
        return playwright.chromium.launch(headless=True, executable_path=str(candidates[0]))
    raise RuntimeError("Chromium missing; run: python -m playwright install chromium")
