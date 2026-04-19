import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page_content(url):
    """
    通用爬取函数：自带Cloudflare绕过，参数 url
    返回：网页源码, 文章正文
    """
    # 配置 专用防检测浏览器（最强破CF）
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # 后台运行
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 启动专用浏览器
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # 等待CF验证自动通过

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
        # 抓取正文（稳定版）
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
    source, content = get_page_content(target_url)
    print("✅ 爬取成功！文章正文：\n")
    print(content)
