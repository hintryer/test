import requests
import re

# 直接用这个固定 URL，不改任何参数！
url = "https://clients2.google.com/service/update2/crx?acceptformat=crx2,crx3&prodversion=130.0.0.0&x=id%3Dhdokiejnpimakedhajhdlcegeplioahd%26uc%26lang%3Dzh-CN%26os%3DWindows%26arch%3Dx64"

try:
    resp = requests.get(url, timeout=15)
    xml = resp.text

    print("=== 官方返回 XML ===")
    print(xml)
    print("====================\n")

    # 安全提取，不报错
    ver_match = re.search(r'version="([0-9a-z.]+)"', xml)
    size_match = re.search(r'size="(\d+)"', xml)

    print("✅ 提取结果：")
    print("版本号：", ver_match.group(1) if ver_match else "未获取到")
    print("文件大小：", size_match.group(1) if size_match else "未获取到")

except Exception as e:
    print("出错：", e)
