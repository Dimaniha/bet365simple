import pyautogui


def is_team1_match():
    if pyautogui.pixelMatchesColor(403, 236, (((56, 216, 120) or (255, 255, 255)))):
        position = True
    elif pyautogui.pixelMatchesColor(305, 236, (((56, 216, 120) or (255, 255, 255)))):
        position = True
    elif pyautogui.pixelMatchesColor(566, 236, (((56, 216, 120) or (255, 255, 255)))):
        position = True
    elif pyautogui.pixelMatchesColor(433, 236, (((56, 216, 120) or (255, 255, 255)))):
        position = True
    else:
        position = False
    return position
