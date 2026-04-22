from lastversion import lastversion
import pprint

# 获取原始数据
latest = lastversion.latest("mautic/mautic", output_format='dict')

# 完整输出（不会丢失任何内容）
print("完整版本信息：")
pprint.pprint(latest, indent=2, width=1000000)
