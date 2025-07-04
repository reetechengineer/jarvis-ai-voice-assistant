#!/usr/bin/env python3
"""
Setup script for Jarvis AI Voice Assistant
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Jarvis AI Voice Assistant - A powerful Python-based voice assistant"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="jarvis-ai-assistant",
    version="2.0.0",
    author="AI Assistant",
    author_email="developer@example.com",
    description="A powerful AI voice assistant built with Python",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jarvis-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Home Automation",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.9.1",
            "flake8>=6.1.0",
        ],
        "optional": [
            "openai>=1.3.5",
            "gtts>=2.4.0",
            "pygame>=2.5.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "jarvis=jarvis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.example"],
    },
    keywords="ai assistant voice recognition speech text-to-speech automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/jarvis-assistant/issues",
        "Source": "https://github.com/yourusername/jarvis-assistant",
        "Documentation": "https://github.com/yourusername/jarvis-assistant/blob/main/README.md",
    },
)