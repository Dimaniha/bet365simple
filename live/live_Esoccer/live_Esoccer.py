import re
from functions import open_link, title_teams_len_check, is_point_clickable_check, full_time_result_check, make_bet, \
    bot, screenshot, Both_Teams_to_Score_check
from live import abandoned_boys
import var
import pyautogui
import time
import datetime


def live_Esoccer(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg):
    if re.search(r'Both Teams to Score', str(bet_option)):
        if re.search(r'no', str(bet_team.lower())):
            bot.send_message(var.uid, f'{var.bot_number}: ОЗ НЕТ - ставку пропускаю.')
            return
        else:
            print('yes')
            open_link(url)
            position = title_teams_len_check(teams)
            if position:
                spoiler_point = [635, 378]
                point = [172, 426]
            else:
                spoiler_point = [635, 348]
                point = [172, 396]
            pyautogui.click(x=spoiler_point[0], y=spoiler_point[1])
            time.sleep(0.5)
            clickable = is_point_clickable_check(point)
            if clickable:
                pyautogui.click(x=point[0], y=point[1])
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg}'
                make_bet(send_msg)
            else:
                return


def live_Esoccer_draw(task, send_msg):
    n = 0
    for line in task:
        if re.search(r'https', str(line)):
            url = line
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line[1:].split('vs')
                n += 1
    open_link(url)
    position = title_teams_len_check(teams)
    print('position', position)
    point = full_time_result_check(position)
    print(point)
    clickable = is_point_clickable_check(point)
    if clickable:
        print('clickable???', )
        pyautogui.click(x=point[0], y=point[1])
        send_msg['msg'] = f'{var.bot_number}: успешно поставил на {task[0][1:]}'
        make_bet(send_msg)
    else:
        return


def live_Esoccer_total(task, send_msg):
    n = 0
    print('live_total')
    print(task, 'task')
    for line in task:
        if line == task[0]:
            bet_option = line[1:]
            print(bet_option)
            if re.search(r'over', str(bet_option.strip().lower())):
                x = 362
                print('over')
            elif re.search(r'under', str(bet_option.strip().lower())):
                x = 488
                print('under')
            bet_team = line[3:].split()[2]
            print(bet_team)
            if bet_team.strip() in abandoned_boys.fifa_total_list:
                bot.send_message(var.uid, f'{var.bot_number}: Тотал на {bet_team} - ставку пропускаю')
                return
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line[2:].split('vs')
                n += 1
            else:
                clubs = line[2:].split('vs')
        elif re.search(r'Current Time', str(line)):
            curr_time = datetime.datetime.strptime(line[-5:], "%M:%S")
            a_timedelta = curr_time - datetime.datetime(1900, 1, 1)
            curr_time_seconds = a_timedelta.total_seconds()
            if curr_time_seconds >= 340:
                send_msg['msg'] = f'{var.bot_number}: время матча больше 5:40 ({a_timedelta}), ставку пропускаю. ' \
                                  f'Скрин на всякий'
                screenshot(send_msg['msg'])
                return
        elif re.search(r'https', str(line)):
            url = line
    teams_len = len(teams)
    print(teams_len)
    open_link(url)
    position = title_teams_len_check(teams)
    if position:
        Both_Teams_to_Score_y_check = 381
    else:
        Both_Teams_to_Score_y_check = 351
    print('position total', position)
    for word in range(0, teams_len):
        if re.match(rf'{bet_team.strip().lower()}', str(teams[word].strip().lower())):
            send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option}'
            if word == 0:  # line 1
                print("line 1")
                y = Both_Teams_to_Score_check(word, Both_Teams_to_Score_y_check)
                point = [x, y]
                break
            else:  # line 2
                print("line 2")
                y = Both_Teams_to_Score_check(word, Both_Teams_to_Score_y_check)
                point = [x, y]
                break
    print(x, y)
    clickable = is_point_clickable_check(point)
    if clickable:
        pyautogui.click(x=point[0], y=point[1])
        make_bet(send_msg)
    else:
        return
