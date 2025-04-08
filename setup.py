# setup.py
from setuptools import setup, find_packages

setup(
    name="chatbuilder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gradio>=4.0.0",  # 推荐使用 Gradio v4+ 的稳定版本
    ],
)
