import os
import json
import requests
import urllib.parse
from playwright.sync_api import sync_playwright
import subprocess  # 用于自动安装
from bs4 import BeautifulSoup

# ==============================================
# 🔥 核心：Python 内部自动安装 Playwright 浏览器
# ==============================================
def install_playwright_browser():
    try:
        print("🔧 检查 Playwright 浏览器...")
        # 自动安装 chromium（Linux 会自动装依赖）
        subprocess.run(
            ["playwright", "install", "--with-deps", "chromium"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Playwright 浏览器准备完成")
    except Exception:
        pass

# 启动时自动安装
install_playwright_browser()


def get_page_content(url):
    with sync_playwright() as p:
        # 启动防检测浏览器
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome 130.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 访问页面 → 自动过 CF 验证
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # 等待验证完成
        
        # 获取页面内容
        html = page.content()
        browser.close()
        
        # 解析正文
        soup = BeautifulSoup(html, "html.parser")
        content = ""
        tag = soup.find("div", id="contentbox")
        if tag:
            content = tag.get_text(separator="\n", strip=False)
        
        return html, content

# ======================
# 测试
# ======================
if __name__ == "__main__":
    url = "https://www.xzwen.com/290733/84.html"
    source, content = get_page_content(url)
    print("===== 正文 =====")
    print(content)
为什么你之前所有方法都失败？
