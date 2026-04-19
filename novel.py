from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_page_content(url):
    """
    通用爬取函数：传入URL，自动绕过CF验证，返回网页源码 + 正文
    """
    chrome_options = Options()
    
    # 核心：必须加这些参数，才能绕过Cloudflare验证
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # 模拟真实浏览器
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # 等待验证自动完成

        # ======================
        # 测试：输出网页源码
        # ======================
        page_source = driver.page_source
        print("=" * 60)
        print("【测试】完整网页源码")
        print("=" * 60)
        print(page_source[:10000])
        print("\n" + "=" * 60 + "\n")

        # ======================
        # 抓取正文（正确选择器）
        # ======================
        wait = WebDriverWait(driver, 20)
        content = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "content"))
        ).text

        return page_source, content

    finally:
        driver.quit()

# ======================
# 测试调用
# ======================
if __name__ == "__main__":
    target_url = "https://www.xzwen.com/290733/84.html"
    
    # 执行抓取
    source, content = get_page_content(target_url)

    # 输出正文
    print("✅ 爬取成功！文章正文：\n")
    print(content)
