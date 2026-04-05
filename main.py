import requests
from bs4 import BeautifulSoup

# 目标网页地址
target_url = "https://www.downkuai.com/soft/70281.html"
# 模拟浏览器请求头（关键，避免被反爬）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://www.downkuai.com/",  # 增加来源页，提升请求合法性
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

try:
    # 1. 请求目标网页，解析出下载API链接
    response = requests.get(target_url, headers=headers, timeout=10)
    response.raise_for_status()  # 抛出请求错误（如404/500）
    soup = BeautifulSoup(response.text, "html.parser")
    # 定位class="btn"的a标签，提取href（即API链接）
    api_link = soup.find("a", class_="btn")["href"]
    print(f"提取到下载API链接：{api_link}")

    # 2. 请求API链接，跟踪302重定向获取真实下载地址
    # allow_redirects=False 先禁止重定向，可查看重定向信息；也可直接设为True，通过response.url获取最终地址
    api_response = requests.get(api_link, headers=headers, allow_redirects=False, timeout=10)
    real_download_url = api_response.headers["Location"]  # 302重定向的真实地址在Location头中
    print(f"获取到真实下载地址：{real_download_url}")

except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
except Exception as e:
    print(f"解析失败：{e}")
