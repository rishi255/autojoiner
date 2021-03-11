# standard imports
import platform
import re
import sys
import time
import subprocess

# third party imports
import importlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# local imports
from .config_user import *
from .__init__ import *

# class URL is passed to this program somehow.
def join_meeting(url: str, browser):	
	browser.get(url)
	
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, "push_download_join_by_browser")))
	webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
	print("Pressed esc")
	browser.find_element_by_id("push_download_join_by_browser").click()
	WebDriverWait(browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="pbui_iframe"]')))
	
	# Enter name and email, click next
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "style-input-2nuAk")))
	name, email = browser.find_elements_by_class_name("style-input-2nuAk")
	name.send_keys(name_to_join_with)		# ! USES an option from config 
	email.send_keys(email_to_join_with)		# ! USES an option from config
	browser.find_element_by_id("guest_next-btn").click()

	# now click ok and join meeting
	try:
		WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Got it")]')))
		browser.find_element_by_xpath('//button[contains(text(), "Got it")]').click()
	except:
		print("Can't find the Got it!")

	# press ALT+A to allow camera and mic permissions.
	print("Wait for 5 sec...")
	time.sleep(5)
	webdriver.ActionChains(browser).key_down(Keys.ALT).send_keys('a').key_up(Keys.ALT).perform()
	print("Pressed ALT+A !!")

	if turn_off_video_before_join: 	# ! USES an option from config
		try:
			WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@data-doi='VIDEO:STOP_VIDEO:MEETSIMPLE_INTERSTITIAL']")))
			browser.find_element_by_xpath("//button[@data-doi='VIDEO:STOP_VIDEO:MEETSIMPLE_INTERSTITIAL']").click()
			print("Found the turn off video button and clicked it!")
		except:
			print("I think video is off already!")

	if mute_before_join: 			# ! USES an option from config
		try:
			browser.find_element_by_xpath("//button[@data-doi='AUDIO:MUTE_SELF:MEETSIMPLE_INTERSTITIAL']").click()
			print("Found the mute button and clicked it!")
		except:
			print("I think it's muted already!")

	try:
		browser.find_element_by_xpath('//button[contains(text(), "Start meeting")]').click()
		print("Started the meeting!")
	except:
		print("Can't find the Start meeting button! It's probably Join meeting then...")

	try:
		browser.find_element_by_xpath('//button[contains(text(), "Join meeting")]').click()
		print("Joined the meeting!")
	except:
		print("Can't find the Join meeting button. It was probably start meeting then...")

# TODO: remove "firefox" default argument from here because it's already the default in config.py, so lol
# TODO: implement browser "chrome"
def start_browser(name="firefox"):
	browser = None

	if name=="firefox":
		profile = webdriver.FirefoxProfile()
		options = webdriver.FirefoxOptions()

		profile.set_preference("browser.download.folderList", 2)
		profile.set_preference("browser.download.manager.showWhenStarting", False)
		profile.set_preference("browser.download.dir", useless_download_directory)
		profile.set_preference("browser.download.lastDir", useless_download_directory)
		profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-msdownload, application/octet-stream")
		
		options.set_preference("permissions.default.camera", 1)
		options.set_preference("permissions.default.microphone", 1)

		browser = webdriver.Firefox(firefox_profile=profile, options=options)

	if name=="chrome":
		raise NotImplementedError()
	
	return browser

def main(url, meeting_platform):

	if meeting_platform == 'webex':
		browser = start_browser(browser_name)	# ! USES an option from config
		if browser is None:
			print("Invalid 'browser_name' setting in config.py!")
		
		curr_os = platform.system()
		if curr_os == 'Windows':
			std_out, std_err = run_command_windows(f"gci {useless_download_directory} -File | where Name -match 'webex(\(\d\))?.exe' | rm")
			# p = subprocess.run(f"powershell -Command \"& {{gci {useless_download_directory} -File | where Name -match 'webex(\(\d\))?.exe' | rm}}\"", check=True)
		elif curr_os == 'Linux':
			p = subprocess.run(f"find {useless_download_directory} -name 'webex(\(\d\))?.exe' -delete", shell=True, check=True)
	#	else,  just ignore as this part isn't very important anyway
		print("Cleared useless downloads")

		join_meeting(url, browser)
	
	elif meeting_platform == 'zoom':
		raise NotImplementedError("Autojoin-v2 doesn't work for Zoom yet!")