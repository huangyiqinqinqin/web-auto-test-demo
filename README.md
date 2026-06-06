# Web 自动化测试（Selenium + Playwright）

## 项目简介
使用 Selenium 和 Playwright 对必应搜索进行自动化测试，支持多组关键词批量执行，自动生成测试报告。

## 功能特性
- **Selenium**：显式等待、JS点击策略、HTML报告、失败截图
- **Playwright**：自动等待、快速执行、截图保存
- **数据驱动**：支持多组关键词批量测试

## 环境配置
```bash
pip install selenium playwright pytest
playwright install
```

## 运行测试
```bash
python test_selenium.py
python test_playwright.py
```

## 测试报告
Selenium：执行后生成 reports/report.html
Playwright：执行后生成截图 search_result.png

## 项目结构
02_web_auto_test/
├── test_selenium.py      # Selenium 脚本
├── test_playwright.py    # Playwright 脚本
├── reports/              # 测试报告目录
│   └── report.html
└── search_result.png     # Playwright 截图
