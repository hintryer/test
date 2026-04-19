import requests
from bs4 import BeautifulSoup
import re
import difflib
import time
from urllib.parse import urlparse, urljoin
from requests.adapters import HTTPAdapter

# ===================== 配置区（可自行调整）=====================
TIMEOUT = 15          # 请求超时
REQUEST_DELAY = 1.5   # 爬取间隔秒数，防封IP
MAX_RETRY = 3         # 失败重试次数
SIMILAR_THRESHOLD = 0.95  # 内容重复判定阈值
MAX_CHAPTERS = 1000   # 最大爬取章节数，防止死循环
# ===============================================================

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 全局会话（带重试，更稳定）
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=MAX_RETRY))
session.mount('https://', HTTPAdapter(max_retries=MAX_RETRY))

# 广告过滤规则
ad_patterns = [
    re.compile(r'请收藏.*?网址.*?', re.I),
    re.compile(r'最新网址.*?', re.I),
    re.compile(r'手机版.*?访问.*?', re.I),
    re.compile(r'广告.*?', re.I),
    re.compile(r'vip会员.*?充值.*?', re.I),
    re.compile(r'『.*?』', re.U),
    re.compile(r'【.*?】', re.U),
]

def clean_ads(text):
    for pat in ad_patterns:
        text = pat.sub('', text)
    return text

# 内容相似度检测
def is_content_similar(content1, content2, threshold=SIMILAR_THRESHOLD):
    clean1 = re.sub(r'\s+', '', content1)
    clean2 = re.sub(r'\s+', '', content2)
    if not clean1 or not clean2:
        return False
    max_len = max(len(clean1), len(clean2))
    if abs(len(clean1)-len(clean2)) / max_len > 0.1:
        return False
    ratio = difflib.SequenceMatcher(None, clean1, clean2).ratio()
    return ratio >= threshold

# 提取章节标题
def get_chapter_title(page_text):
    pattern = re.compile(r"第[0-9一二三四五六七八九十百千]+[章节回页]\s*.*", re.I)
    match = pattern.search(page_text)
    if match:
        return match.group().strip()
    return "未知章节"

# 获取单章内容（优化版）
def get_chapter(url, base_url):
    try:
        resp = session.get(url, headers=headers, timeout=TIMEOUT)
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        chapter_title = get_chapter_title(soup.get_text())

        # 更鲁棒的正文匹配：id 或 class
        content = ""
        content_div = soup.find(
            "div",
            attrs={"id": re.compile(r"content|chapter|text|booktext|novel", re.I)}
        )
        if not content_div:
            content_div = soup.find(
                "div",
                attrs={"class": re.compile(r"content|chapter|text|booktext|novel", re.I)}
            )

        if content_div:
            content = content_div.get_text(separator="\n", strip=True)
            content = clean_ads(content)
            content = re.sub(r'\n+', '\n\n', content).strip()

        # 找下一章（更宽松匹配）
        next_url = None
        next_words = ["下一章", "下一节", "下一页", "后一页", "下页", "→", ">>", "》", "下"]
        for word in next_words:
            a_list = soup.find_all("a", string=lambda s: s and word in str(s).strip())
            for a_tag in a_list:
                href = a_tag.get("href")
                if href and href.strip():
                    next_url = urljoin(base_url, href)
                    break
            if next_url:
                break

        return chapter_title, content, next_url

    except Exception as e:
        print(f"抓取异常：{str(e)}")
        return "异常章节", "", None

# ===================== 主爬取函数（新增）=====================
def crawl_novel(start_url):
    current_url = start_url
    base_url = f"{urlparse(start_url).scheme}://{urlparse(start_url).netloc}"
    chapter_count = 0
    last_content = ""
    crawled_urls = set()  # 防止重复爬取

    # 自动生成保存文件名
    filename = "novel_content.txt"
    print(f"📚 开始爬取小说，结果将保存到：{filename}\n")

    with open(filename, "w", encoding="utf-8") as f:
        while current_url and current_url not in crawled_urls and chapter_count < MAX_CHAPTERS:
            chapter_count += 1
            crawled_urls.add(current_url)

            print(f"🔖 正在抓取第 {chapter_count} 章：{current_url}")
            title, content, next_url = get_chapter(current_url, base_url)

            # 内容为空 / 重复 → 停止
            if not content:
                print("❌ 内容为空，停止爬取")
                break
            if is_content_similar(content, last_content):
                print("✅ 内容重复，已到最新章节，爬取完成")
                break

            # 写入文件
            f.write(f"\n{'='*50}\n")
            f.write(f"{title}\n")
            f.write(f"{'='*50}\n\n")
            f.write(content)
            f.write("\n")
            last_content = content

            print(f"✅ {title} —— 抓取完成\n")
            current_url = next_url
            time.sleep(REQUEST_DELAY)

    print(f"\n🎉 爬取结束！总共抓取 {chapter_count} 章，已保存到 {filename}")

# ===================== 启动入口 =====================
if __name__ == "__main__":
    # 在这里填入你要爬的 **第一章链接**
    target_url = "https://www.example.com/chapter1.html"
    crawl_novel(target_url)
