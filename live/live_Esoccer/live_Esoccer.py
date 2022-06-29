import re
from functions import open_link, title_teams_len_check, is_point_clickable_check, full_time_result_check, make_bet, \
    bot, screenshot, Both_Teams_to_Score_check, search_on_page, teams_icon_cutter
from live import abandoned_boys
import var
import pyautogui
import time
import datetime
from classes import Search


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


def live_Esoccer_fulltime_result(task, send_msg):
    n = 0
    for line in task:
        if re.search(r'https', str(line)):
            url = line
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = teams_icon_cutter(line)
                print(teams)
                n += 1
    if re.search(r'Draw', str(task[0])):
        print('draw')
        x = 370
    else:
        bet_name = task[0].split('-')[1]
        print(bet_name)
        teams_len = len(teams)
        for word in range(0, teams_len):
            if re.match(rf'{bet_name.strip().lower()}', str(teams[word].strip().lower())):
                if word == 0:  # column 1
                    print("column 1")
                    x = 192
                    break
                else:  # column 2
                    print("column 2")
                    x = 600
                    break
    open_link(url)
    sign_to_write = 'fulltime result'
    search_on_page(sign_to_write)
    x_search, y, step = 120, [192, 685], 10
    vs = Search(x_search, y, step)
    point = vs.pixel_match_check_vertical()
    point = [x, point[1]+55]
    print(point)
    clickable = is_point_clickable_check(point)
    if clickable:
        print('clickable???', )
        pyautogui.click(x=point[0], y=point[1])
        send_msg['msg'] = f'{var.bot_number}: успешно поставил на {task[0][2:]}'
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
                x_ = 362
                print('over')
            elif re.search(r'under', str(bet_option.strip().lower())):
                x_ = 488
                print('under')
            bet_team = line[3:].split()[2]
            print(bet_team)
            if bet_team.strip() in abandoned_boys.fifa_total_list:
                bot.send_message(var.uid, f'{var.bot_number}: Тотал на {bet_team} - ставку пропускаю')
                return
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = teams_icon_cutter(line)
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
    open_link(url)
    sign_to_write = f'({bet_team.strip()}) esports goals'
    search_on_page(sign_to_write)
    x, y, step = 186, [351, 685], 10
    vs = Search(x, y, step)
    try:
        point_ = vs.pixel_match_check_vertical()
        point = [x_, point_[1]+80]
        print(point)
        send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option}'
        if point_[1] > 600:
            pyautogui.press('down')
            time.sleep(0.5)
            point[1] = point_[1]
        clickable = is_point_clickable_check(point)
        if clickable:
            pyautogui.click(x=point[0], y=point[1])
            make_bet(send_msg)
        else:
            return
    except:
        send_msg['msg'] = f'{var.bot_number}: ставка исчезла'
        screenshot(send_msg['msg'])
        return


def live_Esoccer_asian_handicap(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg):
    print('handicap football')
    if re.search(r"-|\+", str(bet_team)):
        bet_name = re.split(r"-|\+", str(bet_team))[0]
    else:
        bet_name = bet_team.split()[0]
    print(bet_name)
    if bet_name.strip() in abandoned_boys.esoccer_Fulltime_Asian_Hand_list:
        bot.send_message(var.uid, f'{var.bot_number}: Фора на {bet_name} - ставку пропускаю')
        return
    teams = teams_icon_cutter(teams)
    teams_len = len(teams)
    print(teams)
    open_link(url)
    sign_to_write = 'asian handicap'
    search_on_page(sign_to_write)
    time.sleep(0.2)
    x, y, step = 90, [351, 685], 10
    vs = Search(x, y, step)
    try:
        point_ = vs.pixel_match_check_vertical()
        for word in range(0, teams_len):
            print(f'{teams[word].strip().lower()}')
            if re.match(rf'{bet_name.strip().lower()}', str(teams[word].strip().lower())):
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg}'
                if word == 0:  # column 1
                    print("column 1")
                    point = [258, point_[1]+72]
                    break
                else:  # column 2
                    print("column 2")
                    point = [411, point_[1]+72]
                    break
        if point_[1] > 600:
            pyautogui.press('down')
            time.sleep(0.5)
            point[1] = point_[1]
        clickable = is_point_clickable_check(point)
        if clickable:
            pyautogui.click(x=point[0], y=point[1])
            make_bet(send_msg)
        else:
            return
    except:
        send_msg['msg'] = f'{var.bot_number}: ставка исчезла'
        screenshot(send_msg['msg'])
        return
