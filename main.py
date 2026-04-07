import os
import json
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import urllib3
import zipfile

from updatemode import  load_config
from updatemode import  save_config
from updatemode import  download_file
from updatemode import  check_and_update

# 关闭SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 浏览器伪装
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.baidu.com",
    "Accept-Language": "zh-CN,zh;q=0.9",
}



def extract_exe(zip_path, pattern=".*\\.exe$", new_name=None):
    import os
    import zipfile
    import shutil
    import re

    if not os.path.exists(zip_path):
        print(f"❌ 压缩包不存在：{zip_path}")
        return None

    extract_dir = os.path.dirname(zip_path)
    os.makedirs(extract_dir, exist_ok=True)
    
    final_name = None
    extracted_folder = None

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            regex = re.compile(pattern, re.IGNORECASE)
            
            for filename in zf.namelist():
                if regex.match(filename):
                    zf.extract(filename, extract_dir)
                    source_path = os.path.join(extract_dir, filename)
                    extracted_folder = os.path.dirname(source_path)

                    if new_name is None:
                        final_name = os.path.basename(filename)
                    else:
                        final_name = new_name

                    target_file = os.path.join(extract_dir, final_name)

                    if os.path.exists(target_file):
                        os.remove(target_file)

                    shutil.move(source_path, target_file)
                    print(f"✅ 已提取：{target_file}")
                    break  # 👈 只 break，不 return！

        # 删除空文件夹
        if extracted_folder and os.path.isdir(extracted_folder):
            try:
                os.rmdir(extracted_folder)
            except:
                pass

    except Exception as e:
        print(f"❌ 解压异常：{e}")
        final_name = None

    # 删除压缩包（必须执行）
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
    except:
        pass

    return final_name  # 👈 统一在最后 return
    
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
        
        dl_tag = soup.find("dl", class_="pt_dwload bdxz")
        first_download = ""
        if dl_tag:
            a_tag = dl_tag.find("a")
            if a_tag:
                first_download = a_tag.get("href", "")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.downkuai.com/"
        }
        real_url = ""
        if first_download:
            res = requests.get(first_download, headers=headers, allow_redirects=False, timeout=8, verify=False)
            real_url = res.headers.get("Location", "")
        
        return {
            "urlid": urlid,
            "filename": name + ".zip",
            "version": version,
            "date": date,
            "filesize": size,
            "download_link": real_url,
            "save_dir": save_dir
        }

    except Exception as e:
        print(f"爬取失败: {str(e)}")
        return None

# ==============================
# 主程序
# ==============================
def main():
    config_list = load_config()

    for cfg in config_list:
        print(f"\n=============== 🚀 检查更新：{cfg['filename']} ===============")
        try:
            new_info = get_soft_info(cfg)
            if new_info:

                dl_ok=check_and_update(cfg, new_info)
                
                if dl_ok:
                    new_info["filename"]=extract_exe(os.path.join(new_info["save_dir"], new_info["filename"]))
                    print(new_info["filename"])
                cfg.update(new_info)
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")

    save_config(config_list)

if __name__ == "__main__":
    main()
    print("\n✅ 全部完成")
 
