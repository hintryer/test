from lastversion import lastversion
from packaging import version

latest_mautic_version = lastversion.latest("mautic/mautic", output_format='version', pre_ok=True)

print(f'Latest Mautic version: {latest_mautic_version}')

if latest_mautic_version >= version.parse('1.8.1'):
    print('It is newer')
