import requests
import re

def get_ext_version_and_size(ext_id):
    url = f"https://clients2.google.com/service/update2/crx?acceptformat=crx2,crx3&prodversion=130.0.0.0&x=id%3D{ext_id}%26uc%26lang%3Dzh-CN%26os%3DWindows%26arch%3Dx64"
    
    try:
        resp = requests.get(url, timeout=10)
        xml = resp.text
        print("版本号:", xml)
        # 👇 匹配：version="4.152.3"/>
        ver_match = re.search(r'version="(\d+)"/>', xml)
        print("版本号:", ver_match)
        version = ver_match.group(1)

        # 👇 匹配 size
        size_match = re.search(r'size="(\d+)"', xml)
        print("版本号:", size_match)
        size = size_match.group(1)

        return version, size

    except Exception as e:
        return None, None

# ------------------- 测试 -------------------
if __name__ == "__main__":
    vid = "hdokiejnpimakedhajhdlcegeplioahd"
    version, size = get_ext_version_and_size(vid)
    print("版本号:", version)
    print("文件大小:", size)
