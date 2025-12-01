"""
Setup script for the Seeed MR60BHA2 mmWave sensor library.

Author: AB-Engineering
Date: 2025-11-22
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name='MR60BHXX-driver',
    version='1.0.0',
    author='AB-Engineering',
    description='Python library for Seeed MR60BHA2 mmWave heart rate and breath monitoring sensor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AB-Engineering/MR60BHXX-python-driver',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pyserial>=3.5',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.9',
        ],
    },
    keywords='seeed mmwave sensor heart-rate breath-rate raspberry-pi iot',
    project_urls={
        'Documentation': 'https://github.com/AB-Engineering/MR60BHXX-python-driver',
        'Source': 'https://github.com/AB-Engineering/MR60BHXX-python-driver',
        'Tracker': 'https://github.com/AB-Engineering/MR60BHXX-python-driver/issues',
    },
)
