from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in swiggy_zomato_sync/__init__.py
from swiggy_zomato_sync import __version__ as version

setup(
	name="swiggy_zomato_sync",
	version=version,
	description="Sync Swiggy and Zomato orders to ERPNext POS",
	author="Antigravity",
	author_email="admin@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
