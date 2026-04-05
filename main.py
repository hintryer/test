import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import urllib3
import zipfile  # 补上缺失的导入

# 关闭SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================
# 配置路径
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "softconfig.json")

# 浏览器伪装
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.baidu.com",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# ==============================
# 加载配置
# ==============================
def load_config(file_path=CONFIG_FILE):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except:
        return []

# ==========================
# 核心：标准 namelist + extract 解压
# ==========================
def extract_exe(zip_path, final_name):
    if not os.path.exists(zip_path):
        return
    
    with zipfile.ZipFile(zip_path, "r") as zf:
        files = zf.namelist()
        for f in files:
            if f.lower().endswith(".exe"):
                zf.extract(f, path=".")  # 解压到当前目录
                original_exe = os.path.basename(f)
                if os.path.exists(original_exe):
                    os.rename(original_exe, final_name)
                break

    # 删除压缩包
    if os.path.exists(zip_path):
        os.remove(zip_path)

# ==============================
# 下载文件
# ==============================
def download_file(url, save_dir, filename):
    if not url or url == "未知" or not filename:
        print("下载失败：无效链接或文件名")
        return False

    try:
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        
        print(f"开始下载: {filename}")
        with requests.get(url, stream=True, timeout=60, verify=False, headers=HEADERS) as response:
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"下载完成: {filename}\n")
        return save_path  # 返回文件路径

    except Exception as e:
        print(f"下载失败: {filename} | 错误: {str(e)}")
        return None

# ==============================
# 获取软件最新信息
# ==============================
def get_soft_info(config):
    urlid = config["urlid"]
    save_dir = config["save_dir"]
    target_url = f"https://www.downkuai.com/soft/{urlid}.html"

    try:
        response = requests.get(target_url, headers=HEADERS, timeout=15, verify=False)
        response.raise_for_status()
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("a", class_="new_pro_name")
        name = title_tag.get_text(strip=True) if title_tag else "未知"
        version = re.search(r'v[\d.]+', name).group() if "v" in name else "未知"
        
        spa_spans = soup.find("div", class_="newPro_spa").find_all("span") if soup.find("div", class_="newPro_spa") else []
        size = spa_spans[0].get_text(strip=True) if len(spa_spans)>=1 else "未知"
        date = spa_spans[2].get_text(strip=True) if len(spa_spans)>=3 else "未知"
        
        dl_tag = soup.find("dl", class_="pt_dwload")
        first_download = ""
        if dl_tag:
            a_tag = dl_tag.find("a")
            if a_tag:
                first_download = a_tag.get("href", "")

        filename = f"{name.replace(' ', '_').replace('/', '_')}_{version}.zip"
        headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Referer": "https://www.downkuai.com/"
                    }
        res = requests.get(first_download, headers=headers, allow_redirects=False, timeout=8)
        real_url = res.headers.get("Location")
        return {
            "urlid": urlid,
            "name": name,
            "filename": filename,
            "version": version,
            "date": date,
            "size": size,
            "download_link": real_url,
            "save_dir": save_dir
        }

    except Exception as e:
        print(f"爬取失败: {str(e)}")
        return None

# ==============================
# 版本对比 + 更新下载
# ==============================
def check_and_update(cfg, new_info):
    old_version = cfg.get("version", "")
    new_version = new_info["version"]
    download_url = new_info["download_link"]
    filename = new_info["filename"]
    save_dir = new_info["save_dir"]

    print(f"当前版本: {old_version} → 最新版本: {new_version}")

    if new_version == old_version:
        if os.path.exists(os.path.join(save_dir, filename)):
            print("✅ 已是最新版本")
            return False, None
        else:
            print("⚠️ 文件丢失，重新下载...")
            zip_path = download_file(download_url, save_dir, filename)
            return True, zip_path

    print("🔄 发现新版本，开始更新...")
    zip_path = download_file(download_url, save_dir, filename)

    if zip_path:
        old_file = cfg.get("filename", "")
        old_path = os.path.join(save_dir, old_file)
        if old_file and os.path.exists(old_path) and old_path != os.path.join(save_dir, filename):
            try:
                os.remove(old_path)
                print("🗑️ 已删除旧版本文件")
            except:
                pass
        print("✅ 更新成功")
        return True, zip_path
    return False, None

# ==============================
# 主程序
# ==============================
def main():
    config_list = load_config()
    if not config_list:
        config_list = [{
            "urlid": "152759",
            "name": "FastStone",
            "filename": "",
            "version": "",
            "date": "",
            "size": "",
            "download_link": "",
            "save_dir": "./download"
        }]

    for cfg in config_list:
        print(f"\n=============== 🚀 检查更新：{cfg['name']} ===============")
        try:
            new_info = get_soft_info(cfg)
            if new_info:
                dl_ok, zip_path = check_and_update(cfg, new_info)
                if dl_ok and zip_path:
                    print("🔓 开始解压exe...")
                    extract_exe(zip_path, "FastStone.exe")  # 重命名
                cfg.update(new_info)
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
    print("\n✅ 全部完成")
