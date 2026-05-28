#!/usr/bin/env python3
import re
from pathlib import Path
from setuptools import setup


def read(fname):
    return Path(__file__).with_name(fname).read_text(encoding="utf-8")


def get_version():
    version_path = Path(__file__).resolve().parents[2] / "include" / "mega" / "version.h"
    version_file = version_path.read_text(encoding="utf-8")

    major_match = re.search(r"#define\s+MEGA_MAJOR_VERSION\s+(\d+)", version_file)
    minor_match = re.search(r"#define\s+MEGA_MINOR_VERSION\s+(\d+)", version_file)
    patch_match = re.search(r"#define\s+MEGA_MICRO_VERSION\s+(\d+)", version_file)

    major = major_match.group(1) if major_match else "0"
    minor = minor_match.group(1) if minor_match else "0"
    patch = patch_match.group(1) if patch_match else "0"

    version = f"{major}.{minor}.{patch}"

    return version


setup(
    name="megasdk",
    version=get_version(),
    description="Python bindings to the Mega file storage SDK.",
    long_description_content_type="text/x-rst",
    long_description=read("DESCRIPTION.rst"),
    url="http://github.com/meganz/sdk/",
    license="Simplified BSD",
    author="Guy Kloss",
    author_email="gk@mega.co.nz",
    python_requires=">=3.8",
    packages=["mega"],
    package_dir={"mega": "."},
    package_data={
        "mega": ["_mega.*", "_SDKPythonBindings.*", "mega.py"],
    },
    include_package_data=True,
    keywords=["MEGA", "privacy", "cloud", "storage", "API"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)