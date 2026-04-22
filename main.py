from lastversion import lastversion
from packaging import version

latest_mautic_version = lastversion.latest("mautic/mautic", output_format='dict')

print(f'Latest Mautic version: {latest_mautic_version}')
