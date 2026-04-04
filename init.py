import os
from datetime import datetime, timedelta

# 设置 GitHub 环境变量
def set_github_env(env_name, env_value):
    """
    通用函数：向 GitHub Actions 环境变量写入值
    :param env_name: 环境变量名，如 COMMIT_TIME
    :param env_value: 环境变量内容
    """
    github_env_path = os.getenv("GITHUB_ENV")
    if github_env_path:
        with open(github_env_path, "a", encoding="utf-8") as f:
            f.write(f"{env_name}={env_value}\n")
        print(f"✅ 已设置环境变量 {env_name} = {env_value}")
        
# 写入任意文件
def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(content) + "\n")

def main():
    beijingtime = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    set_github_env("COMMIT_TIME", f"Update: {beijingtime}")
    write_file("data.txt", beijingtime)
    
# 在 main 最后调用
if __name__ == "__main__":
    main()
    print("\n✅ 全部完成")
