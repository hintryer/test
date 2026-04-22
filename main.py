import requests
import re

# LastPass 插件 ID
EXT_ID = "hdokiejnpimakedhajhdlcegeplioahd"

# 谷歌官方更新 API（不下载，只查信息）
url = f"https://clients2.google.com/service/update2/crx?prodversion=120&x=id%3D{EXT_ID}%26uc"

try:
    # 获取官方 XML 信息
    resp = requests.get(url, timeout=10)
    xml = resp.text

    # 正则提取 版本号
    ver_match = re.search(r'version="([0-9.]+)"', xml)
    version = ver_match.group(1) if ver_match else "未知"

    # 正则提取 文件大小（字节）
    size_match = re.search(r'size="(\d+)"', xml)
    size_bytes = int(size_match.group(1)) if size_match else 0
    size_mb = round(size_bytes / 1024 / 1024, 2)

    # 输出结果
    print("✅ 插件信息获取成功")
    print(f"版本号：{version}")
    print(f"文件大小：{size_bytes} 字节 ({size_mb} MB)")

except Exception as e:
    print(f"出错：{e}")
