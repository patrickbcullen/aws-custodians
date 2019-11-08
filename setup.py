import os
from setuptools import setup, find_packages
import warnings

setup(
    name='aws-custodians',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'boto3>=1.10.13',
        'Click>=7.0'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    entry_points={
        "console_scripts": [
            "aws-custodians=custodians.cli:cli",
        ]
    },
    namespace_packages = ['custodians'],
    author="Patrick Cullen",
    author_email="patrickbcullen@gmail.com",
    url="https://github.com/patrickbcullen/aws-custodians",
    download_url = "https://github.com/patrickbcullen/aws-custodians/tarball/v0.1.0",
    keywords = ['custodians', 'aws'],
    classifiers = []
)
