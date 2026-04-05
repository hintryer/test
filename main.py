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

    li = soup.find("li")

    # 提取
    title = li.find("a", class_="new_pro_name").get_text(strip=True)
    link = li.find("a", class_="new_pro_name")["href"]
    spa_spans = li.find("div", class_="newPro_spa").find_all("span")
    size = spa_spans[0].get_text(strip=True)
    date = spa_spans[2].get_text(strip=True)
    
    # 输出
    print("提取完成：")
    print(f"名称：{title}")
    print(f"版本：v8.3")
    print(f"大小：{size}")
    print(f"日期：{date}")
    print(f"链接：{link}")
    print("===== 爬取成功 =====")
    print(soup)


except requests.exceptions.RequestException as e:
    print(f"网络请求失败：{e}")
    print("\n解决方法：")
    print("1. 检查网络是否能正常打开网页")
    print("2. 打开浏览器访问：https://www.downkuai.com/soft/152759.html")
    print("3. 如果浏览器能打开，代码不能打开 → 开启代理")
