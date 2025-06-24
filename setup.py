"""
Mapiry - A comprehensive Python SDK for Mapillary API v4
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mapiry",
    version="1.0.0",
    author="tikisn",
    author_email="s2501082@sendai-nct.jp",
    description="A comprehensive Python SDK for Mapillary API v4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tikipiya/Mapiry",
    project_urls={
        "Bug Tracker": "https://github.com/tikipiya/Mapiry/issues",
        "Documentation": "https://github.com/tikipiya/Mapiry/blob/main/README.md",
        "Source Code": "https://github.com/tikipiya/Mapiry",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="mapillary, api, sdk, street-view, imagery, computer-vision, gis",
    include_package_data=True,
    zip_safe=False,
)