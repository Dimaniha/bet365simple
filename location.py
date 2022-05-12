import pyautogui
import time


def location():  # определение коорд указателя для тестов
    time.sleep(7)
    # pyautogui.moveTo(612, 462)
    n = pyautogui.position()
    print(n)
    pix = pyautogui.pixel(n[0], n[1])
    print(pix)
    time.sleep(40)


location()
