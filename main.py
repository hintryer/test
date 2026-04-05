from bs4 import BeautifulSoup
import requests

# 你提供的 HTML 代码（本地下载地址区域）
html = '''
<dl class="pt_dwload bdxz">
<dt>本地下载地址：</dt>
<dd><a href="https://get.downkuai.com/download/70281/38" target="_blank" rel="nofollow"><i></i><span>浙江电信下载</span></a></dd>
<dd><a href="https://get.downkuai.com/download/70281/37" target="_blank" rel="nofollow"><i></i><span>广东电信下载</span></a></dd>
<dd><a href="https://get.downkuai.com/download/70281/39" target="_blank" rel="nofollow"><i></i><span>北京联通下载</span></a></dd>
<dd><a href="https://get.downkuai.com/download/70281/40" target="_blank" rel="nofollow"><i></i><span>上海电信下载</span></a></dd>
</dl>
'''

# 1. 解析 HTML，提取所有下载链接
soup = BeautifulSoup(html, "html.parser")
download_links = []

# 找到所有 <a> 标签
for a in soup.select(".pt_dwload a"):
    name = a.get_text(strip=True)  # 线路名：浙江电信下载等
    href = a["href"]               # 中间链接
    download_links.append((name, href))

# 2. 请求每个中间链接，获取 真实下载地址（302跳转）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.downkuai.com/"
}

print("===== 真实下载地址 =====")
for name, link in download_links:
    try:
        # 禁止自动跳转，拿到真实地址
        res = requests.get(link, headers=headers, allow_redirects=False, timeout=8)
        real_url = res.headers.get("Location")
        
        if real_url:
            print(f"✅ {name}")
            print(f"   真实地址：{real_url}\n")
        else:
            print(f"❌ {name}：链接失效\n")
            
    except Exception as e:
        print(f"❌ {name}：获取失败 {str(e)}\n")
