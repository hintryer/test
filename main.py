import requests
import re

ext_id = "hdokiejnpimakedhajhdlcegeplioahd"

url = (
    "https://clients2.google.com/service/update2/crx"
    "?acceptformat=crx2,crx3"
    "&prodversion=130.0.0.0"
    "&x=id%3D{id}%26uc%26lang%3Dzh-CN"
).format(id=ext_id)

try:
    resp = requests.get(url, timeout=10)
    xml = resp.text
    print("=== XML ===")
    print(xml)
    print("===========")

    # 安全提取
    ver = re.search(r'version="([0-9.]+)"', xml)
    size = re.search(r'size="(\d+)"', xml)

    print("版本:", ver.group(1) if ver else "未返回")
    print("大小:", size.group(1) if size else "未返回")

except Exception as e:
    print("错误:", e)
