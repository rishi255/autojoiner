# standard imports
from datetime import datetime
import platform
import re
import subprocess

# third party imports
import click
from click.exceptions import ClickException
import importlib

# local imports
# autojoin = importlib.import_module(".autojoin", "src")
from . import autojoin
from .__init__ import *

#! Link validation regex patterns
webex_link_pattern =  "(^.*[.]webex[.].*$)"
zoom_link_pattern = ""

############### CLICK FUNCTIONS ###############
@click.group()
def main():
	"""Autojoiner CLI"""
	pass
    
@main.command()
@click.argument("meeting_link")
@click.argument("date", type=click.DateTime(["%Y-%m-%d"]))
@click.argument("time", type=click.DateTime(["%H:%M"]))
@click.argument("name") # name of task
@click.option("-r", "--repeat-weekly", is_flag=True, default=False, help="If used, means that this link needs to be joined every week at the specified day and time.")
def add(meeting_link, date, time, repeat_weekly, name):
	date_time = datetime.combine(date.date(), time.time())
	print(f"Meeting link: {meeting_link}, Dateime = {date_time}, repeat weekly = {repeat_weekly}")

	if validate_link(meeting_link) is None:
		raise Exception(f"{meeting_link} not a valid link!")
	
	curr_os = platform.system()
	if curr_os == 'Windows':
		#! use "schtasks" command to add task to Windows Scheduler

		#! Just check if name already exists
		std_out, std_err = run_command_windows(f"schtasks /query /fo CSV /tn \"autojoin_tasks\\{name}\"")

		print(f"stdout: {std_out}")
		print(f"stderr: {std_err}")

		if "ERROR: The system cannot find the file specified." not in std_err[0]:
			raise click.ClickException("Task with that name already exists!")
		else:
			print("The name doesn't already exist! Need to create the task now.")
			if repeat_weekly:
				cmd = f"schtasks /create /sc WEEKLY /d {get_weekday_code(date_time.isoweekday())} /st {date_time.strftime('%H:%M')} /tn \"autojoin_tasks\\{name}\" /tr \"powershell -Command autojoiner join {meeting_link}; sleep 10\" /f"
			else:
				cmd = f""

			print(f"Running command: '{cmd}'")
			std_out, std_err = run_command_windows(cmd)
			print("After running:")
			print(f"stdout: {std_out}")
			print(f"stderr: {std_err}")
		
		#! Nope, below commented out part useless for now. Name is mandatory to pass.
			# first find next available name IF name is not passed
			# if name == "":
			# 	output = subprocess.run(["powershell", "-Command", "schtasks /query /fo CSV /tn \"autojoin_tasks\\\" | findstr \"autojoin_task\""], stdout=subprocess.PIPE).stdout.decode('utf-8')
			# 	output = output.split('\n')[:-1] # discard empty element at the end (since it ends with '\n')
			# 	if output[0][:7] == "ERROR: ": # not found
			# 		output = "default"
			# 	else:
			# 		# get last line of output, then extract name 
			# 		output = output[-1].split()[0]
			# 		# now output will only contain taskname.
				
			# 	print(output)

	elif curr_os == 'Linux':
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
	autojoin.main(meeting_link, meeting_platform)

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

def get_weekday_code(dayno):
	if dayno == 0:
		return "MON"
	elif dayno == 1:
		return "TUE"
	elif dayno == 2:
		return "WED"
	elif dayno == 3:
		return "THU"
	elif dayno == 4:
		return "FRI"
	elif dayno == 5:
		return "SAT"
	elif dayno == 6:
		return "SUN"

if __name__ == '__main__':
    main()