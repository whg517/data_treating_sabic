import re
from os.path import dirname, join

from setuptools import find_packages, setup

with open(join(dirname(__file__), 'data_treating_sabic/__init__.py'), "rt", encoding="utf8") as f:
    version = re.search(r"__VERSION__ = '(.*?)'", f.read()).group(1)

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

EXCLUDE_FROM_PACKAGES = ['tests', 'docs']

setup(
    name='data_treating_sabic',
    version=version,
    author='wanghuagang',
    author_email="huagang517@126.com",
    description="data treating sabic",
    keywords='data treating sabic',
    url='',
    platforms='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 1 - Planning",
        "Natural Language :: Chinese (Simplified)",
    ],
)
