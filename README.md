# autojoiner

[![PyPI version](https://img.shields.io/pypi/v/autojoiner?style=flat-square)](https://pypi.org/project/autojoiner)
[![PyPI downloads](https://img.shields.io/pypi/dd/autojoiner?style=flat-square)](https://pypistats.org/packages/autojoiner)
![PyPI license](https://img.shields.io/pypi/l/autojoiner?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/rishi255/autojoiner?style=flat-square)

A CLI tool to automate the joining of Zoom or Cisco Webex meetings at scheduled times irrespective of operating system.

Uses Selenium to automate the joining of meetings, and uses Task Scheduler or `schtasks` (Windows) / `crontab` (Linux) to schedule meetings.

## Currently supported features

- Schedule the joining of a meeting:  
  `autojoiner add [--repeat-weekly] <meeting_link> <start date> <time to join> <task name>`  
  where,

  - start date is in format YYYY-MM-DD
  - time is in format HH:mm

- Immediately join a meeting (automated using Selenium):  
  `autojoiner join <meeting_link>`

## How to install

[This package is hosted on PyPi](https://pypi.org/project/autojoiner/), which means installation as simple as running one command: `pip install autojoiner`
