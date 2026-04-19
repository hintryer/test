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
    """
    传入 url，自动过 Cloudflare
    返回：完整网页源码, 完整正文（id=chaptercontent）
    """
    with sync_playwright() as p:
        # 最强防检测浏览器（自动过CF）
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        # 模拟真实浏览器
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome 140.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(6000)  # 等CF验证完成
        
        # 获取完整网页源码
        full_html = page.content()
        
        # 提取正文（id=chaptercontent）
        soup = BeautifulSoup(full_html, "html.parser")
        content = ""
        chapter_tag = soup.find("div", id="chaptercontent")
        if chapter_tag:
            content = chapter_tag.get_text(separator="\n", strip=False)
        
        browser.close()
    
    # 返回：完整源码 + 完整正文
    return full_html, content

# ======================
# 测试：输出所有内容
# ======================
if __name__ == "__main__":
    target_url = "https://www.xzwen.com/290733/84.html"
    
    # 调用函数
    html_source, article_content = get_page_content(target_url)
    
    # ==========================================
    # 输出 1：完整网页源码
    # ==========================================
    print("=" * 80)
    print("📄 完整网页源码")
    print("=" * 80)
    print(html_source)
    
    # ==========================================
    # 输出 2：完整正文（chaptercontent）
    # ==========================================
    print("\n" + "=" * 80)
    print("📖 文章正文（id=chaptercontent）")
    print("=" * 80)
    print(article_content)
