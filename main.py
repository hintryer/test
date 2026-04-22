import requests
import re

# 插件 ID
EXT_ID = "hdokiejnpimakedhajhdlcegeplioahd"

# 谷歌官方 API 地址
url = f"https://clients2.google.com/service/update2/crx?prodversion=120&x=id%3D{EXT_ID}%26uc"

try:
    # 发送请求
    resp = requests.get(url, timeout=10)
    
    # ==============================================
    # 👇 直接输出 完整官方 XML 内容
    # ==============================================
    print("=" * 50)
    print("📄 官方返回的 XML 信息：")
    print("=" * 50)
    print(resp.text)  # 这一行就是输出原始 XML
    print("=" * 50)

    # 从 XML 里提取版本号 & 大小
    xml = resp.text
    ver = re.search(r'version="([0-9.]+)"', xml).group(1)
    size = re.search(r'size="(\d+)"', xml).group(1)
    size_mb = round(int(size) / 1024 / 1024, 2)

    print(f"\n✅ 提取结果：")
    print(f"版本号：{ver}")
    print(f"文件大小：{size} 字节（{size_mb} MB）")

except Exception as e:
    print("请求失败：", e)
