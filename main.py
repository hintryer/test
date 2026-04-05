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

    # 提取标题 + 链接
    title_tag = soup.find("a", class_="new_pro_name")
    if title_tag:
        name = title_tag.get_text(strip=True)
        link = title_tag.get("href", "未知")
    
    # 提取大小、日期
    spa_div = soup.find("div", class_="newPro_spa")
    if spa_div:
        spans = spa_div.find_all("span")
        if len(spans) >= 1:
            size = spans[0].get_text(strip=True)
        if len(spans) >= 3:
            date = spans[2].get_text(strip=True)
    
    # 自动提取版本号（从名称里截取 v开头的版本）
    if "v" in name:
        import re
        ver_match = re.search(r'v[\d.]+', name)
        if ver_match:
            version = ver_match.group()
    dl_tag = soup.find("dl", class_="pt_dwload bdxz")
    if dl_tag:
        a_tag = dl_tag.find("a")  # 只找第一个a标签
        if a_tag:
            first_link = a_tag.get("href", "")
    # 输出结果
    print("✅ 提取成功")
    print(f"软件名称：{name}")
    print(f"版本：{version}")
    print(f"大小：{size}")
    print(f"日期：{date}")
    print(f"详情链接：{first_link}")
    print("===== 爬取成功 =====")
    print(soup)


except requests.exceptions.RequestException as e:
    print(f"网络请求失败：{e}")
    print("\n解决方法：")
    print("1. 检查网络是否能正常打开网页")
    print("2. 打开浏览器访问：https://www.downkuai.com/soft/152759.html")
    print("3. 如果浏览器能打开，代码不能打开 → 开启代理")
