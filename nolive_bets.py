import re
import time

from functions import *


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
        x, y = 350, [192, 685]
        point = pixel_match_check_vertical(x, y)
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
        else:
            continue
    sign_to_write = 'full time result'
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('backspace')
    search_on_page(sign_to_write)
    x_list = [262, 654]
    y_list = [337, 386, 369, 418]
    point = full_time_result_check_on_page(x_list, y_list)
    is_point_clickable_check(point)
    print('clickable???')
    pyautogui.click(x=point[0], y=point[1])
    make_bet(send_msg)


def nolive_table_tennis(url, bet_option, sport_type, send_msg):
    option = bet_option.split()[0]
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {sport_type} - {bet_option}'
    open_link(url)
    if option == 'o':
        point = [614, 451]
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(2)
        make_bet(send_msg)
    elif option == 'u':
        point = [878, 451]
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(2)
        make_bet(send_msg)


def nolive_soccer(url, bet_option, sport_type):
    pass


def nolive_ice_hockey(url, bet_option, sport_type):
    pass


def nolive_basketball(url, bet_option, sport_type):
    pass


def nolive_bet_from_image(image_path):
    white_line_range, width = get_white_line_range(image_path)
    last_y_position = len(white_line_range) - 1
    coordinates = [0, white_line_range[0], width, white_line_range[last_y_position]]
    crop_a_particular_place(coordinates, image_path, masks.nolive_white_line)
    result = text_recognition(masks.nolive_white_line)

