import os
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "crxconfig.json")

def load_config(file_path=CONFIG_FILE):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except (json.JSONDecodeError, ValueError):
        return []

def download_file(url, save_dir, filename):
    if not url or not filename:
        print("下载失败：未获取到有效链接或文件名")
        return False

    try:
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        
        print(f"开始下载: {filename}")
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"下载完成: {filename}\n")
        return True

    except Exception as e:
        print(f"下载失败: {filename} | 错误: {str(e)}")
        return False


def check_and_update(cfg, new_info):
    old_version = cfg.get("version", "")
    last_version = new_info["version"]
    download_url = new_info["download_link"]
    asset_filename = new_info["filename"]
    save_dir = new_info["save_dir"]
    filesize = new_info["filesize"]

    current_file_path = os.path.join(save_dir, asset_filename)
    old_file_path = os.path.join(save_dir, cfg.get("filename", ""))

    MAX_SIZE_MB = 100
    is_file_too_big = filesize > MAX_SIZE_MB

    print(f"当前版本: {old_version} → 最新版本: {last_version}")
    if is_file_too_big:
        print(f"⚠️ 文件过大({filesize:.2f}MB)，仅更新版本信息")

    # 版本相同
    if last_version == old_version:
        if os.path.exists(current_file_path) or is_file_too_big:
            print("✅ 已是最新版本")
            return False
        else:
            print("⚠️ 文件丢失，重新下载...")
            return download_file(download_url, save_dir, asset_filename)

    # 需要更新
    dl_ok = True
    if not is_file_too_big:
        dl_ok = download_file(download_url, save_dir, asset_filename)
        if dl_ok:
            if os.path.exists(old_file_path) and old_file_path != current_file_path:
                try:
                    os.remove(old_file_path)
                    print("🗑️ 已删除旧文件")
                except:
                    pass
            print("✅ 更新成功")
    else:
        print("✅ 版本信息已更新（文件过大未下载）")

    return dl_ok

def main():

if __name__ == "__main__":
    main()
