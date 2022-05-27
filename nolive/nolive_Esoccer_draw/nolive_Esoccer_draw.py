import re
from functions import open_link, search_on_page, is_point_clickable_check, make_bet, \
    screenshot, full_time_result_check_on_page
from nolive_Esoccer_draw_functions import *
from classes import Search
import var
import time


def nolive_Esoccer_draw(task, send_msg):
    n = 0
    print('taskk', task)
    for line in task:
        if re.search(r'https', str(line)):
            url = line
            print(url)
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line[2:].split('vs')
                n += 1
            else:
                clubs = line[2:].split('vs')
    for iter in range(5):
        open_link(url)
        sign_to_write = f'{clubs[1].strip()[:-1]} ({teams[1].strip()}) esports'
        search_on_page(sign_to_write)
        if iter != 0:
            pyautogui.press('enter', presses=iter)
        x, y, step = 350, [192, 685], 3
        vs = Search(x, y, step)
        point = vs.pixel_match_check_vertical()
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(2)
        sign_to_write = f'({teams[0].strip()}) esports'
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.hotkey('backspace')
        search_on_page(sign_to_write)
        team1 = is_team1_match()
        print('position', team1)
        if team1:
            break
        elif iter == 4 and not team1:
            send_msg['msg'] = f'{var.bot_number}: совпадений не найдено'
            screenshot(send_msg['msg'])
            return
        else:
            continue
    sign_to_write = 'full time result'
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('backspace')
    search_on_page(sign_to_write)
    x_list = [262, 654]
    y_list = [337, 386, 369, 418]
    point = full_time_result_check_on_page(x_list, y_list)
    clickable = is_point_clickable_check(point)
    if clickable:
        pyautogui.click(x=point[0], y=point[1])
        make_bet(send_msg)
    else:
        return
