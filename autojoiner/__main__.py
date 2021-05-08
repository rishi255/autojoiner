# standard imports
# local imports
import configparser
import os
import platform
import re
import subprocess
from datetime import datetime
from pathlib import Path

# third party imports
import click
from click.exceptions import ClickException

from . import autojoin
from .__init__ import *

#! Link validation regex patterns
webex_link_pattern = "(^.*[.]webex[.].*$)"
zoom_link_pattern = ""

# default config options
config_obj = configparser.ConfigParser()
config_obj["autojoiner-config"] = {
    "name_to_join_with": "User",
    "email_to_join_with": "",
    "mute_before_join": True,
    "turn_off_video_before_join": True,
    "browser_name": "firefox",
    "useless_download_directory": "",
}

############### CLICK FUNCTIONS ###############
@click.group()
def main():
    """Autojoiner-v2 CLI"""
    # if config file doesn't exist create it
    config_file = Path(os.path.join(Path.home(), ".autojoinerconf"))
    if config_file.is_file() and os.stat(config_file).st_size:
        config_obj.read(config_file)
    else:
        with open(config_file, "w") as f:
            config_obj.write(f)


@main.command()
@click.argument("meeting_link")
@click.argument("date", type=click.DateTime(["%Y-%m-%d"]))
@click.argument("time", type=click.DateTime(["%H:%M"]))
@click.argument("name")  # name of task
@click.option(
    "-r",
    "--repeat-weekly",
    is_flag=True,
    default=False,
    help="If used, means that this link needs to be joined every week at the specified day and time.",
)
def add(meeting_link, date, time, repeat_weekly, name):
    date_time = datetime.combine(date.date(), time.time())
    print(
        f"Meeting link: {meeting_link}, Datetime = {date_time}, repeat weekly = {repeat_weekly}"
    )

    if validate_link(meeting_link) is None:
        raise Exception(f"{meeting_link} not a valid link!")

    curr_os = platform.system()
    if curr_os == "Windows":
        #! use "schtasks" command to add task to Windows Scheduler

        #! Just check if name already exists
        std_out, std_err = run_command_windows(
            f'schtasks /query /fo CSV /tn "autojoin_tasks\\{name}"'
        )

        print(f"stdout: {std_out}")
        print(f"stderr: {std_err}")

        if "ERROR: " not in std_err[0].strip():
            raise click.ClickException("Task with that name already exists!")
        else:
            print("The name doesn't already exist! Need to create the task now.")

            sc = "WEEKLY" if repeat_weekly else "ONCE"
            cmd = (
                f"schtasks /create /sc {sc} /sd {datetime.strftime(datetime.now().date(), '%m/%d/%Y')} "
                f"/st {date_time.strftime('%H:%M')} /tn \"autojoin_tasks\\{name}\" "
                f"/tr \"powershell -Command autojoiner join '{meeting_link}'; exit;\" /f"
            )

            print(f"Running command: '{cmd}'")
            std_out, std_err = run_command_windows(cmd)
            print("After running:")
            print(f"stdout: {std_out}")
            print(f"stderr: {std_err}")

    elif curr_os == "Linux":
        raise NotImplementedError("Sorry, this tool isn't supported on your OS yet!")
    else:
        raise NotImplementedError("Sorry, this tool isn't supported on your OS yet!")


@main.command()
@click.argument("meeting_link")
def join(meeting_link):
    print(f"JOIN CALLED on link {meeting_link}! Joining now using Selenium.")

    meeting_platform = validate_link(meeting_link)
    if meeting_platform is None:
        raise Exception(f"{meeting_link} not a valid link!")

    # now call the Selenium code in autojoin.py
    autojoin.main(meeting_link, meeting_platform, config_obj)


@main.command()
def info():
    print(platform.system())


############### OTHER FUNCTIONS ###############


def validate_link(text):
    if bool(re.match(webex_link_pattern, text)):
        return "webex"
    elif bool(re.match(zoom_link_pattern, text)):
        return "zoom"
    else:
        return None


# def get_weekday_code(dayno):
#     if dayno == 0:
#         return "MON"
#     elif dayno == 1:
#         return "TUE"
#     elif dayno == 2:
#         return "WED"
#     elif dayno == 3:
#         return "THU"
#     elif dayno == 4:
#         return "FRI"
#     elif dayno == 5:
#         return "SAT"
#     elif dayno == 6:
#         return "SUN"


if __name__ == "__main__":
    main()
