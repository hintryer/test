import requests

EXT_ID = "hdokiejnpimakedhajhdlcegeplioahd"
version = "4.152.3"  # 上面获取到的版本号
save_folder = "lastpass"

# 创建文件夹
import os
os.makedirs(save_folder, exist_ok=True)

# 下载链接（官方）
dl_url = f"https://clients2.google.com/service/update2/crx?response=redirect&acceptformat=crx3&x=id%3D{EXT_ID}%26uc"
save_path = f"{save_folder}/LastPass_{version}.crx"

# 开始下载
with requests.get(dl_url, stream=True, timeout=20) as r:
    r.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print(f"下载完成：{save_path}")
