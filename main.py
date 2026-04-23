import requests

# 软件名列表
apps = [
    "MouseClickTool",
    "notepad4",
    "MusicPlayer2",
    "VideoCaptioner",
    "scribe2srt",
    "ffmpeg_batch",
    "lanzouyun-disk",
    "localsend",
    "Bili23-Downloader",
    "clash-verge-rev",
    "codexffmpeg",
    "git"
]

url_pattern = "https://raw.githubusercontent.com/duzyn/scoop-cn/refs/heads/master/bucket/{}.json"

merged = []

for app in apps:
    url = url_pattern.format(app)
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        content = resp.json()
        merged.append({
            "filename": f"{app}.json",
            "content": content
        })
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")

# merged 结果即为你要的格式
import json
print(json.dumps(merged, ensure_ascii=False, indent=2))
