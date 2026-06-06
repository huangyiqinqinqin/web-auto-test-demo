from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.bing.com")

    # 找到搜索框，点击它
    page.click("textarea[name='q']")

    # 逐字输入，每个字间隔0.3秒
    for char in "测试":
        page.keyboard.type(char)
        time.sleep(0.3)

    # 停顿1秒，让你看清输入的内容
    time.sleep(1)

    # 按回车搜索
    page.keyboard.press("Enter")

    page.wait_for_timeout(2000)
    page.screenshot(path="search_result.png")
    print("搜索完成，截图已保存")
    browser.close()