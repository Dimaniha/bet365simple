import re
from functions import *


def nolive_Esoccer_draw(task, send_msg):
    n = 0
    for line in task:
        if re.search(r'https', str(line)):
            url = line
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line[1:].split('vs')
                n += 1
    open_link(url)

    pyautogui.click(x=557, y=382)
    time.sleep(1)
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