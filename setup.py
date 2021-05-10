from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="autojoiner",
    packages=["autojoiner"],
    description=long_description,
    long_description_content_type="text/markdown",
    version="0.2.1",
    install_requires=[
        "click",
        "selenium",
    ],
    python_requires=">=3.8",
    entry_points="""
        [console_scripts]
        autojoiner=autojoiner.__main__:main
    """,
    author="Rishikesh Rachchh",
    author_email="rishikeshrachchh@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    url="https://github.com/rishi255/autojoiner",
)
