import time
import var
import pyautogui
import telebot
import re


pyautogui.FAILSAFE = False
bot = telebot.TeleBot(var.API_TOKEN)


def open_link(name):
    pyautogui.click(x=681, y=93)
    time.sleep(0.1)
    pyautogui.write(name)
    time.sleep(0.1)
    pyautogui.click(x=458, y=282)
    time.sleep(2)
    pyautogui.click(x=49, y=254)
    time.sleep(0.1)
    pyautogui.click(x=686, y=203)
    return


def screenshot(send_msg):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(var.feedback_screenshot)
    bot.send_photo(var.uid, open(var.feedback_screenshot, 'rb'), caption=send_msg)


def teams_icon_cutter(line):
    for i in range(len(line)):
        if re.match(r'\w', str(line[i])):
            teams = line[i:].split('vs')
            print(teams)
            return teams
