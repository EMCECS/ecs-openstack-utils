from setuptools import setup, find_packages

setup(
    name='ecsmgmt',
    version='0.1.1',
    packages=find_packages(),
    scripts=['ecs_admin_client.py'],
    url='https://github.com/EMCECS/ECS-CommunityEdition',
    license='EMC',
    author='joshia7',
    author_email='',
    description='Python ECS Management SDK',
    install_requires=[
        'requests',
        'simplejson',
        'PyYAML',
        'httplib2',
        'ipaddress',
        'futures',
        'pyopenssl',
    ],
)
