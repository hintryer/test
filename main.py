import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

target_url = "https://www.downkuai.com/soft/152759.html"

# 超强浏览器伪装
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.baidu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close",
}

# 如果你本地有代理，把下面的端口改成你自己的
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

try:
    # 方案1：如果你有代理，用这一行（取消注释）
    # response = requests.get(target_url, headers=headers, proxies=proxies, timeout=10)

    # 方案2：无代理，直接请求（国内网络可用）
    response = requests.get(target_url, headers=headers, timeout=15, verify=False)

    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    # 提取信息
    version = soup.find(string=lambda s: s and "版本：" in s).replace("版本：", "").strip()
    date = soup.find(string=lambda s: s and "日期：" in s).replace("日期：", "").strip()
    download_btn = soup.find("a", class_="btn")
    download_link = urljoin(target_url, download_btn.get("href"))
    size = download_btn.text.replace("立即下载 ", "").strip()

    print("===== 爬取成功 =====")
    print(f"版本：{version}")
    print(f"大小：{size}")
    print(f"日期：{date}")
    print(f"下载链接：{download_link}")

except requests.exceptions.RequestException as e:
    print(f"网络请求失败：{e}")
    print("\n解决方法：")
    print("1. 检查网络是否能正常打开网页")
    print("2. 打开浏览器访问：https://www.downkuai.com/soft/152759.html")
    print("3. 如果浏览器能打开，代码不能打开 → 开启代理")
