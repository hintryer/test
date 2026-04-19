from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 1. 配置Chrome选项（无头模式，不弹出浏览器窗口）
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 2. 初始化浏览器
driver = webdriver.Chrome(options=chrome_options)

try:
    # 目标网址
    url = "https://www.xzwen.com/290733/84.html"
    driver.get(url)
    time.sleep(1)  # 等待页面加载

    # 3. 定位正文区域（根据网页结构定位）
    # 该网站正文在 class="content" 的 div 下
    content = driver.find_element(By.CLASS_NAME, "content").text

    # 4. 输出结果
    print("========== 爬取到的正文内容 ==========")
    print(content)

finally:
    # 关闭浏览器
    driver.quit()
