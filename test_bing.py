from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# 测试数据：多组关键词
test_keywords = ["测试", "selenium", "自动化测试"]

# 创建报告文件夹
if not os.path.exists("reports"):
    os.makedirs("reports")

# 初始化浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# 打开必应
driver.get("https://www.bing.com")
print("=" * 50)
print("开始执行测试")
print("=" * 50)

# 等待页面加载
time.sleep(2)

# 统计结果
passed = 0
failed = 0
results = []  # 保存结果用于生成报告

for keyword in test_keywords:
    print(f"\n▶ 测试关键词：{keyword}")

    try:
        # 方法1：用 name 属性定位搜索框（更通用）
        try:
            search_box = driver.find_element(By.NAME, "q")
        except:
            # 方法2：用 CSS 选择器
            search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search']")

        # 清空并输入关键词
        search_box.clear()
        search_box.send_keys(keyword)
        time.sleep(0.5)

        # 方法1：用 Enter 键提交（比找搜索按钮更稳定）
        search_box.submit()

        # 等待结果加载
        time.sleep(2)

        # 验证：检查页面标题是否包含关键词
        title = driver.title
        if keyword in title:
            print(f"   ✅ 验证通过 - 页面标题包含'{keyword}'")
            passed += 1
            results.append({"keyword": keyword, "status": "✅ 通过", "title": title})
        else:
            print(f"   ❌ 验证失败 - 页面标题为：{title}")
            screenshot_path = f"reports/fail_{keyword}.png"
            driver.save_screenshot(screenshot_path)
            print(f"   📸 截图已保存：{screenshot_path}")
            failed += 1
            results.append({"keyword": keyword, "status": "❌ 失败", "title": title})

    except Exception as e:
        print(f"   ❌ 执行异常：{str(e)[:100]}")
        screenshot_path = f"reports/error_{keyword}.png"
        driver.save_screenshot(screenshot_path)
        print(f"   📸 错误截图：{screenshot_path}")
        failed += 1
        results.append({"keyword": keyword, "status": "⚠️ 异常", "title": str(e)[:50]})

    # 回到首页，准备下一个测试
    driver.get("https://www.bing.com")
    time.sleep(1)

# 关闭浏览器
driver.quit()

# 打印测试报告
print("\n" + "=" * 50)
print("测试报告")
print("=" * 50)
print(f"总计测试数：{len(test_keywords)}")
print(f"✅ 通过：{passed}")
print(f"❌ 失败：{failed}")
print(f"通过率：{passed / len(test_keywords) * 100}%")
print("=" * 50)

# 生成 HTML 报告
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>必应搜索自动化测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 20px 0; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .error {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>🔍 必应搜索自动化测试报告</h1>
    <div class="summary">
        <p><strong>执行时间：</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>总计测试数：</strong> {len(test_keywords)}</p>
        <p><strong>✅ 通过：</strong> {passed}</p>
        <p><strong>❌ 失败：</strong> {failed}</p>
        <p><strong>📊 通过率：</strong> {passed / len(test_keywords) * 100:.1f}%</p>
    </div>
    <table>
        <tr>
            <th>状态</th>
            <th>关键词</th>
            <th>页面标题/信息</th>
        </tr>
"""
for r in results:
    status_class = "pass" if "通过" in r["status"] else ("fail" if "失败" in r["status"] else "error")
    html_content += f"""
        <tr>
            <td class="{status_class}">{r["status"]}</td>
            <td>{r["keyword"]}</td>
            <td>{r["title"]}</td>
        </tr>"""
html_content += """
    </table>
    <hr>
    <p><small>报告生成时间：""" + time.strftime('%Y-%m-%d %H:%M:%S') + """</small></p>
</body>
</html>"""

with open("reports/report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n📄 HTML报告已生成：reports/report.html")
print("💡 用浏览器打开 reports/report.html 查看美观的测试报告")