"""captura uma página real no navegador: url e arquivo de saída."""
import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    page.goto(sys.argv[1], wait_until='domcontentloaded', timeout=90000)
    page.wait_for_timeout(15000)
    print(page.locator('body').inner_text()[:6000])
    page.screenshot(path=sys.argv[2], full_page=True)
    browser.close()
