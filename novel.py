from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page_content(url):
    """
    通用爬取函数：传入URL，返回网页源码 + 正文内容
    """
    # 浏览器配置（无头模式，服务器环境也能用）
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开网页
        driver.get(url)

        # ======================
        # 测试：输出 完整网页源码
        # ======================
        page_source = driver.page_source
        print("=" * 60)
        print("【测试】完整网页源码：")
        print("=" * 60)
        print(page_source[:10000])  # 只打印前10000字符，避免太多
        print("\n" + "=" * 60 + "\n")

        # ======================
        # 等待并抓取正文
        # ======================
        wait = WebDriverWait(driver, 15)
        content_element = wait.until(
            EC.presence_of_element_located((By.ID, "contentbox"))
        )
        content_text = content_element.text

        return page_source, content_text

    finally:
        driver.quit()

# ======================
# 测试调用
# ======================
if __name__ == "__main__":
    target_url = "https://www.xzwen.com/290733/84.html"
    
    # 调用函数
    source, content = get_page_content(target_url)

    # 输出正文
    print("【爬取成功】文章正文：\n")
    print(content)
