import importlib
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_stealth import stealth

from .__init__ import *

TIMEOUT_PERIOD = 5

# class URL is passed to this program somehow.
def join_webex_meeting(
    url: str,
    browser,
    config_object,
):
    name_to_join_with = config_object["name_to_join_with"]
    email_to_join_with = config_object["email_to_join_with"]
    mute_before_join = config_object["mute_before_join"]
    turn_off_video_before_join = config_object["turn_off_video_before_join"]

    browser.get(url)

    WebDriverWait(browser, TIMEOUT_PERIOD).until(
        EC.presence_of_element_located((By.ID, "push_download_join_by_browser"))
    )
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    browser.find_element_by_id("push_download_join_by_browser").click()

    print("Clicked on join from browser!")

    WebDriverWait(browser, TIMEOUT_PERIOD).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, "/html/body/section/iframe")
        )
    )

    print("Found the iframe where the input fields are!")

    # Enter name and email, click next
    WebDriverWait(browser, TIMEOUT_PERIOD).until(
        EC.presence_of_element_located((By.CLASS_NAME, "style-input-2nuAk"))
    )
    name, email = browser.find_elements_by_class_name("style-input-2nuAk")
    name.send_keys(name_to_join_with)  # ! USES an option from config
    email.send_keys(email_to_join_with)  # ! USES an option from config
    browser.find_element_by_id("guest_next-btn").click()

    print("Clicked on Next!")

    # now click ok and join meeting
    try:
        WebDriverWait(browser, TIMEOUT_PERIOD).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(), "Got it")]')
            )
        )
        browser.find_element_by_xpath('//button[contains(text(), "Got it")]').click()
    except:
        print("Can't find the Got it!")

    # press ALT+A to allow camera and mic permissions.
    print("Wait for 5 sec...")
    browser.implicitly_wait(5)
    # webdriver.ActionChains(browser).key_down(Keys.ALT).send_keys("a").key_up(
    #     Keys.ALT
    # ).perform()
    # print("Pressed ALT+A !!")

    if turn_off_video_before_join:  # ! USES an option from config
        try:
            WebDriverWait(browser, TIMEOUT_PERIOD).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[@data-doi='VIDEO:STOP_VIDEO:MEETSIMPLE_INTERSTITIAL']",
                    )
                )
            )
            browser.find_element_by_xpath(
                "//button[@data-doi='VIDEO:STOP_VIDEO:MEETSIMPLE_INTERSTITIAL']"
            ).click()
            print("Found the turn off video button and clicked it!")
        except:
            print("Video is (likely) off already!")

    if mute_before_join:  # ! USES an option from config
        try:
            browser.find_element_by_xpath(
                "//button[@data-doi='AUDIO:MUTE_SELF:MEETSIMPLE_INTERSTITIAL']"
            ).click()
            print("Found the mute button and clicked it!")
        except:
            print("You're (likely) already muted!")

    try:
        browser.find_element_by_xpath(
            '//button[contains(text(), "Start meeting")]'
        ).click()
        print("Started the meeting!")
    except:
        print("Can't find the Start meeting button! It's probably Join meeting then...")

    try:
        browser.find_element_by_xpath(
            '//button[contains(text(), "Join meeting")]'
        ).click()
        print("Joined the meeting!")
    except:
        print("Can't find the Join meeting button either!. Something is wrong.")


#! CAN'T USE THIS FUNCTION ANYMORE.
def join_google_meeting(
    url: str,
    browser,
    config_object,
):
    def Glogin(mail_address, password):
        # input Gmail
        browser.get("https://accounts.google.com/")
        browser.find_element_by_id("identifierId").send_keys(mail_address)
        browser.find_element_by_id("identifierNext").click()
        browser.implicitly_wait(10)

        # input Password
        browser.find_element_by_xpath(
            '//*[@id="password"]/div[1]/div/div[1]/input'
        ).send_keys(password)
        browser.implicitly_wait(10)
        browser.find_element_by_id("passwordNext").click()
        browser.implicitly_wait(10)

        # go to google home page
        browser.get("https://google.com/")
        browser.implicitly_wait(100)

    gmail_address = config_object["gmail_address"]
    gmail_password = config_object["gmail_password"]
    mute_before_join = config_object["mute_before_join"]
    turn_off_video_before_join = config_object["turn_off_video_before_join"]

    Glogin(gmail_address, gmail_password)
    browser.get(url)
    browser.implicitly_wait(10)
    browser.implicitly_wait(10)


# TODO: implement browser "chrome"
def start_browser(name):
    browser = None

    if name == "firefox":
        profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()

        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        # profile.set_preference("browser.download.dir", useless_download_directory)
        # profile.set_preference("browser.download.lastDir", useless_download_directory)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/x-msdownload, application/octet-stream",
        )

        options.set_preference("permissions.default.camera", 1)
        options.set_preference("permissions.default.microphone", 1)

        log_path = "nul" if platform.system() == "Windows" else "/dev/null"
        browser = webdriver.Firefox(
            firefox_profile=profile, options=options, service_log_path=log_path
        )

    if name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option("useAutomationExtension", False)
        browser = webdriver.Chrome(chrome_options=options)

    return browser


# def get(config_obj, key):
#     return config_obj["autojoiner-config"].get(key, None)


def main(url, meeting_platform, config_obj):
    if meeting_platform == "webex":
        x = config_obj[meeting_platform]
        browser = start_browser(x["browser_name"])  # ! USES an option from config
        if browser is None:
            print("Invalid 'browser_name' setting in ~/.autojoinerconf!")

        useless_download_directory = x["useless_download_directory"]

        curr_os = platform.system()
        if curr_os == "Windows":
            std_out, std_err = run_command_windows(
                f"gci {useless_download_directory} -File | where Name -match 'webex(\(\d\))?.exe' | rm"
            )
            # p = subprocess.run(f"powershell -Command \"& {{gci {useless_download_directory} -File | where Name -match 'webex(\(\d\))?.exe' | rm}}\"", check=True)
        elif curr_os == "Linux":
            p = subprocess.run(
                f"find {useless_download_directory} -name 'webex(\(\d\))?.exe' -delete",
                shell=True,
                check=True,
            )
        # 	else,  just ignore as this part isn't very important anyway
        print("Cleared useless downloads")

        join_webex_meeting(url, browser, config_obj["webex"])

    elif meeting_platform == "meet":
        raise NotImplementedError(
            "Not supported due to security limitations for automated Google sign-in."
        )
        # x = config_obj[meeting_platform]
        # browser = start_browser(x["browser_name"])  # ! USES an option from config
        # if browser is None:
        #     print("Invalid 'browser_name' setting in ~/.autojoinerconf!")

        # join_google_meeting(url, browser, config_obj["meet"])

    elif meeting_platform == "zoom":
        raise NotImplementedError("Autojoin-v2 doesn't work for Zoom yet!")
