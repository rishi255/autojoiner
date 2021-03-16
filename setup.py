from setuptools import setup

setup(
    name='autojoiner',
    packages=['autojoiner'],
    # description='',
    version='0.0.4',
    install_requires=[
        'click', 
        'selenium',
    ],
     extras_require={
        'gui': ['PyAutoGUI'], # this doesn't exist on TestPyPi, hence creates issues -> Made it optional
    },
    python_requires='>=3.8',
    entry_points='''
        [console_scripts]
        autojoiner=autojoiner.__main__:main
    ''',
    author="Rishikesh Rachchh",
    author_email="rishikeshrachchh@gmail.com",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',

    ],
    license='MIT',
    url="https://github.com/rishi255/autojoiner"
)
