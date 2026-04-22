from lastversion import lastversion
import json

# 获取最新版本（完整字典，不会丢失数据）
latest = lastversion.latest("mautic/mautic", output_format='dict')

# 打印完整内容（不会被截断）
print("完整版本信息：")
print(json.dumps(latest, indent=4, ensure_ascii=False))

# 写入文件（最关键）
with open("version_info.json", "w", encoding="utf-8") as f:
    json.dump(latest, f, indent=4, ensure_ascii=False)

print("\n✅ 已完整写入到 version_info.json")
