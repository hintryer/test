import os
import json


def load_config(file_path="config.json"):
    """加载配置文件，安全容错"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(base_dir, file_path)
    
    if not os.path.exists(config_file_path):
        return []
    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
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
    """版本对比 + 智能更新"""
    old_version = cfg.get("version", "")
    last_version = new_info.get("version", "")
    download_url = new_info.get("download_link", "")
    asset_filename = new_info.get("filename", "")
    save_dir = new_info.get("save_dir", "./download")
    filesize = new_info.get("filesize", "0 MB")

    current_file_path = os.path.join(save_dir, asset_filename)
    old_file_path = os.path.join(save_dir, cfg.get("filename", ""))

    # 修复：字符串不能直接和数字比较
    file_mb = parse_filesize_mb(filesize)
    MAX_SIZE_MB = 100
    is_file_too_big = file_mb > MAX_SIZE_MB

    print(f"当前版本: {old_version} → 最新版本: {last_version}")
    if is_file_too_big:
        print(f"⚠️ 文件过大({file_mb:.2f}MB)，仅更新版本信息")

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
                except Exception:
                    pass
            print("✅ 更新成功")
    else:
        print("✅ 版本信息已更新（文件过大未下载）")

    return dl_ok

def main():

if __name__ == "__main__":
    main()
