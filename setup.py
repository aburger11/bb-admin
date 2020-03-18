from setuptools import setup, find_packages

setup(
    name='bb-admin',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==7.0',
        'PyYAML==5.3',
        'requests==2.23.0',
        'deepmerge==0.1.0'
    ],
    entry_points='''
        [console_scripts]
        bb-admin=scripts.init:cli
    ''',
)
