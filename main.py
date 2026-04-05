import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

target_url = "https://www.downkuai.com/soft/152759.html"

# 超强浏览器伪装
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.baidu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "close",
}


try:
   
    response = requests.get(target_url, headers=headers, timeout=15, verify=False)

    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    # 名称
    title_tag = soup.find("a", class_="new_pro_name")
    name = title_tag.get_text(strip=True) if title_tag else "未知"
    
    # 版本
    version = re.search(r'v[\d.]+', name).group() if "v" in name else "未知"
    
    # 大小 + 日期
    spa_spans = soup.find("div", class_="newPro_spa").find_all("span") if soup.find("div", class_="newPro_spa") else []
    size = spa_spans[0].get_text(strip=True) if len(spa_spans)>=1 else "未知"
    date = spa_spans[2].get_text(strip=True) if len(spa_spans)>=3 else "未知"
    
    # 第一个下载地址
    first_download = soup.find("dl", class_="pt_dwload").find("a").get("href", "") if soup.find("dl", class_="pt_dwload") and soup.find("dl", class_="pt_dwload").find("a") else "未知"
    
    # ------------ 输出 ------------
    print("软件名称：", name)
    print("版本：", version)
    print("大小：", size)
    print("日期：", date)
    print("第一个下载地址：", first_download)
    print("===== 爬取成功 =====")
    print(soup)


except requests.exceptions.RequestException as e:
    print(f"网络请求失败：{e}")
