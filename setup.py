from setuptools import setup

setup(
    name='autojoiner',
    packages=['autojoiner'],
    # description='',
    version='2.0.3',
    install_requires=[
        'click', 'pyautogui', 'selenium',
    ],
    python_requires='>=3.8',
    entry_points='''
        [console_scripts]
        autojoiner=autojoiner.__main__:main
    ''',
    author="Rishikesh Rachchh",
    author_email="rishikeshrachchh@gmail.com",
    license='MIT',
    url="https://github.com/rishi255/autojoin-v2",
    download_url='https://github.com/rishi255/autojoin-v2/archive/v2.tar.gz',
    # dependency_links=dependency_links
)
