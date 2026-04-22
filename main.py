from lastversion import lastversion
import sys

# 确保 Python 输出不截断、不缓冲
sys.displayhook = sys.__displayhook__

# 获取原始数据
latest = lastversion.latest("mautic/mautic", output_format='dict')

# 【完整输出】不截断、不省略、不格式化、不修改
print("完整版本信息：")
print(repr(latest))
