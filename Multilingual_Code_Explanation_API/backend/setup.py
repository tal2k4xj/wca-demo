from setuptools import setup, find_packages
import os
from pathlib import Path

# Read requirements from requirements.txt
def read_requirements(filename: str) -> list:
    """Read requirements from file"""
    reqs_path = Path(__file__).parent / filename
    with open(reqs_path, 'r', encoding='utf-8') as f:
        reqs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return reqs

setup(
    name="wca_i18n",
    version="0.1.0",
    packages=find_packages(include=['wca_i18n', 'wca_i18n.*']),
    python_requires=">=3.8",
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-asyncio>=0.18.0',
            'httpx>=0.23.0',
            'aiohttp>=3.8.0',
            'reportlab>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'wca-i18n=wca_i18n.main:main',
        ],
    },
) 