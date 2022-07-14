import time
import var
import pyautogui
import telebot
import re


pyautogui.FAILSAFE = False
bot = telebot.TeleBot(var.API_TOKEN)


def open_link(name):
    pyautogui.click(x=681, y=93)
    time.sleep(1)
    pyautogui.write(name)
    time.sleep(4)
    match = game_check()
    if not match:
        return False
    pyautogui.click(x=458, y=282)
    time.sleep(2)
    pyautogui.click(x=49, y=254)
    time.sleep(0.1)
    return True


def one_click_bet_check():
    pyautogui.click(x=726, y=128)
    time.sleep(2)
    if pyautogui.pixelMatchesColor(683, 206, (48, 150, 209)):
        return
    else:
        pyautogui.click(x=683, y=206)
        time.sleep(2)


def game_check():
    if pyautogui.pixelMatchesColor(813, 266, (251, 251, 251)):
        send_msg = 'Матч не найден'
        screenshot(send_msg)
        pyautogui.hotkey('esc')
        return False
    else:
        return True


def scrollbar_position_check():
    pyautogui.moveTo(1021, 123)
    if pyautogui.pixelMatchesColor(1021, 123, (246, 248, 249)):
        pyautogui.click(clicks=2)


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
