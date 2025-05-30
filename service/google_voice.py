import os
import time
import pygame
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from constants import RECIPIENT_EMAIL, CHROME_EXE_PATH, CHROME_DATA_DIRECTORY
from myemail import email
from mysay import print_say

from script import run_script
from thread_with_exception import thread_with_exception

chrome_options = Options()
chrome_options.add_argument(f"--binary_location={CHROME_EXE_PATH}")
# headless doesn't seem to work, oh well
# chrome_options.add_argument("-headless")
chrome_options.add_argument(f"--user-data-dir={CHROME_DATA_DIRECTORY}")
browser = webdriver.Chrome(options=chrome_options)

browser.get(f"https://voice.google.com")

while True:
    # wait for a call
    button = None
    while not button:
        try:
            button = browser.find_element(
                By.XPATH, '/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-call-sidebar/div/gv-in-call-ng2/div/div/section/div[2]/gv-call-response/div/div[2]/button')
        except NoSuchElementException:
            pass
    print("got a call answer button!")
    caller = "caller"
    number = ""
    try:
        caller = browser.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-call-sidebar/div/gv-in-call-ng2/div/div/section/div[1]/div/gv-in-call-remote-party/div/div[2]').text
        number = browser.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-call-sidebar/div/gv-in-call-ng2/div/div/section/div[1]/div/gv-in-call-remote-party/div/div[4]').text
        if number != "":
            caller = f"{caller} {number}"
    except Exception as e:
        print(e)
    # answer the call
    time.sleep(.6)
    button.click()
    pygame.mixer.init()
    print_say("Incoming call", halt=True)
    pygame.mixer.quit()
    time.sleep(.4)
    try:
        t1 = thread_with_exception(
            'script thread', target=run_script, args=(caller,))
        t1.start()
        # assume the call is active so long as the hang-up button is present
        new_button = browser.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-call-sidebar/div/gv-in-call-ng2/div/div/section/div[2]/gv-call-response/div/div/button')
        while new_button:
            try:
                new_button = browser.find_element(
                    By.XPATH, '/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-call-sidebar/div/gv-in-call-ng2/div/div/section/div[2]/gv-call-response/div/div/button')
            except NoSuchElementException:
                print("hang-up button dissappeared! Exit the script thread.")
                t1.raise_exception()
                break
        t1.join()
    except Exception as e:
        resp = "Well that was an unexpected error. Refrain from doing what you did, Hang up and try again."
        print_say(resp)
        print(e)

    subject = f"{caller} call transcript".replace('\n', '').replace('\r', '')
    email(file="file.txt", recipient=RECIPIENT_EMAIL, subline=subject,
          content="this is what was recorded")

    pygame.mixer.quit()
