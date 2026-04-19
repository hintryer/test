from curl_cffi import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    # 【关键】impersonate="chrome120" 直接模拟真实浏览器，过CF
    resp = requests.get(
        url,
        impersonate="chrome120",
        timeout=20
    )
    
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    
    # 抓取正文
    content = ""
    content_tag = soup.find("div", id="contentbox")
    if content_tag:
        content = content_tag.get_text(strip=False, separator="\n")
    
    return html, content

# ======================
# 测试
# ======================
if __name__ == "__main__":
    url = "https://www.xzwen.com/290733/84.html"
    source, content = get_page_content(url)
    
    print("===== 网页源码 =====")
    print(source[:10000])
    print("\n===== 正文内容 =====")
    print(content)
