from setuptools import setup

setup(
    name='my_cli_tool',
    version='0.1',
    py_modules=['remi_cli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        remi-cli=remi_cli:remi_cli
    ''',
)