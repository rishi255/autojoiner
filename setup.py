from setuptools import setup
# from io import open
# from os import path

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='autojoiner',
    version='2.0',
    packages=['autojoiner'],
    install_requires=[
        'click', 'pyautogui', 'selenium', 'cryptography'
    ],
    python_requires='>=2.7',
    entry_points='''
        [console_scripts]
        autojoiner=src.__main__:main
    ''',
    author="Rishikesh Rachchh",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/rishi255/autojoin-v2",
    author_email="rishikeshrachchh@gmail.com",
    # dependency_links=dependency_links
)
