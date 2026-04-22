import requests
import re

def get_chrome_ext_info(ext_id):
    """
    获取 Chrome 插件官方版本号 + 文件大小
    :param ext_id: 插件ID
    :return: (版本号version, 大小size)
    """
    url = (
        "https://clients2.google.com/service/update2/crx"
        "?acceptformat=crx2,crx3"
        "&prodversion=130.0.0.0"
        "&x=id%3D{id}%26uc%26lang%3Dzh-CN%26os%3DWindows%26arch%3Dx64"
    ).format(id=ext_id)

    try:
        resp = requests.get(url, timeout=15)
        xml = resp.text

        # 正确匹配版本号（修复你之前匹配到 1.0 的BUG）
        ver_match = re.search(r'version="(\d+\.\d+\.\d+)"', xml)
        size_match = re.search(r'size="(\d+)"', xml)

        version = ver_match.group(1) if ver_match else None
        size = size_match.group(1) if size_match else None

        return version, size

    except Exception as e:
        return None, None


# ------------------- 使用示例 -------------------
if __name__ == "__main__":
    ext_id = "hdokiejnpimakedhajhdlcegeplioahd"
    ver, size = get_chrome_ext_info(ext_id)

    print("✅ 插件信息：")
    print(f"版本号：{ver}")
    print(f"文件大小：{size} 字节")

    
    ver_match = re.search(r'version="([0-9a-z.]+)"', xml)
    size_match = re.search(r'size="(\d+)"/>'', xml)

    print("✅ 提取结果：")
    print("版本号：", ver_match.group(1) if ver_match else "未获取到")
    print("文件大小：", size_match.group(1) if size_match else "未获取到")

except Exception as e:
    print("出错：", e)
