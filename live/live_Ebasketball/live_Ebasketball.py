import re
from functions import open_link, title_teams_len_check, is_point_clickable_check, make_bet, bot, teams_icon_cutter
from live import abandoned_boys
import var
import pyautogui
import time


def live_Ebasketball(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg):
    if re.search(r'Fulltime Asian Hand', str(bet_option)):
        print("hand")
        bet_name = re.split(r"-|\+", str(bet_team))[0]
        if bet_name.strip() in abandoned_boys.ebasket_Fulltime_Asian_Hand_list:
            bot.send_message(var.uid, f'{var.bot_number}: Фора на {bet_name} - ставку пропускаю')
            return
        teams = teams_icon_cutter(teams)
        teams_len = len(teams)
        print(teams)
        open_link(url)
        position = title_teams_len_check(teams)
        if position:
            y = 454
        else:
            y = 424
        for word in range(0, teams_len):
            if re.match(rf'{bet_name.strip().lower()}', str(teams[word].strip().lower())):
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg}'
                if word == 0:  # column 1
                    print("column 1")
                    point = [286, y]
                    break
                else:  # column 2
                    print("column 2")
                    point = [491, y]
                    break
        clickable = is_point_clickable_check(point)
        if clickable:
            pyautogui.click(x=point[0], y=point[1])
            make_bet(send_msg)
        else:
            return


def live_Ebasketball_total_halftime(task, send_msg):
    print('total basket half')
    for line in task:
        if line == task[0]:
            bet_option = line[2:]
            print(bet_option)
            if re.search(r'over', str(bet_option.strip().lower())):
                x = 282
                print('over')
            elif re.search(r'under', str(bet_option.strip().lower())):
                x = 606
                print('under')
        elif re.search(r'https', str(line)):
            url = line
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option}'
    open_link(url)
    point = [x, 480]
    pyautogui.click(x=111, y=324)
    time.sleep(1)
    clickable = is_point_clickable_check(point)
    if clickable:
        pyautogui.click(x=point[0], y=point[1])
        make_bet(send_msg)
    else:
        return


def live_Ebasketball_total_fulltime(task, send_msg):
    print('total basket fulltime')
    for line in task:
        if line == task[0]:
            bet_option = line[2:]
            print(bet_option)
            if re.search(r'over', str(bet_option.strip().lower())):
                x = 282
                print('over')
            elif re.search(r'under', str(bet_option.strip().lower())):
                x = 606
                print('under')
        elif re.search(r'https', str(line)):
            url = line
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option}'
    open_link(url)
    point = [x, 491]
    time.sleep(1)
    clickable = is_point_clickable_check(point)
    if clickable:
        pyautogui.click(x=point[0], y=point[1])
        make_bet(send_msg)
    else:
        return
