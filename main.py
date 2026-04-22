from lastversion import lastversion
import json

# 获取最新版本（完整字典，不会丢失数据）
latest = lastversion.latest("mautic/mautic", output_format='dict')

# 打印完整内容（不会被截断）
print("完整版本信息：")
print(latest)
