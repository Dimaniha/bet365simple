import time

import pyautogui

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


def nolive_bet_from_image(task, send_msg, locker, pq):
    try:
        pyautogui.hotkey(var.start_video_hotkey)
        image_path = task[1]
        white_line_range, width = get_white_line_range(image_path)
        last_y_position = len(white_line_range) - 1
        coordinates = [0, white_line_range[0], width, white_line_range[last_y_position]]
        crop_a_particular_place(coordinates, image_path, masks.nolive_white_line)
        result = text_recognition(masks.nolive_white_line)
        result = spaces_delete(result)
        urls = ['https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/', 'https://www.bet365.com/#/AC/B1/C1/D1002/E72260052/G938/'
                ]
        #8 min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/'
        #10min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E72260052/G938/'
        #12min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E71755872/G938/'
        teams = [result[2][:len(result[2]) // 2], result[2][len(result[2]) // 2:]]
        team1 = teams[0].split('(')[1].split(')')[0].lower()
        team2 = teams[1].split('(')[1].split(')')[0].lower()
        print(team1, team2)
        for team in tips_4_screenshots_bets.nicknames:
            if team1 == team:
                team1 = tips_4_screenshots_bets.nicknames[team]
            elif team2 == team:
                team2 = tips_4_screenshots_bets.nicknames[team]
        print(team1, team2)
        for url in range(len(urls)):
            click = False
            n = 0
            while not click:
                open_link(urls[url])
                pyautogui.click(372, 304)
                time.sleep(3)
                pyautogui.click(355, 393)
                time.sleep(3)
                sign_to_write = f'({team2}) esports'
                search_on_page(sign_to_write)
                if n != 0:
                    pyautogui.press('enter', presses=n)
                y, step = [192, 685], 3
                for x in range(400, 470, 30):
                    vs = Search(x, y, step)
                    point = vs.pixel_match_check_vertical()
                    if point:
                        pyautogui.click(x=point[0], y=point[1])
                        time.sleep(3)
                        break
                time.sleep(2)
                click, n = match_page_clickable_check(locker, n)
                if not click:
                    pyautogui.hotkey('f5')
                    time.sleep(3)
                    continue
                sign_to_write = f'({team1}) esports'
                pyautogui.hotkey('ctrl', 'f')
                pyautogui.hotkey('backspace')
                search_on_page(sign_to_write)
                x, y, step = [110, 590], 250, 10
                hs = Search(x, y, step)
                team1 = hs.pixel_match_check_horizontal()
                print('position', team1)
                if team1:
                    print('nashel team1')
                    exitflag = True
                    break
                elif n == 3 and not team1:
                    break
                else:
                    n += 1
                    continue
            if exitflag:
                if url == len(urls) - 1 and not team1:
                    send_msg['msg'] = f'{var.bot_number}: после 3 попыток совпадений не найдено'
                    screenshot(send_msg['msg'])
                    return
                else:
                    break
        sign_to_write, bet_type = image_sign_to_write_determining(result)
        if sign_to_write == 'all':
            sign_to_write = ['popular', 'all']
            for i in sign_to_write:
                point = tab_check(i)
                if point:
                    break
        else:
            point = tab_check(sign_to_write)
        print('point')
        if not point:
            send_msg['msg'] = f'{var.bot_number}: не нашел нужную вкладку'
            screenshot(send_msg['msg'])
            return
        pyautogui.click(x=point[0], y=point[1])  # открыл нужную вкладку на странице
        time.sleep(1)
        point = image_point_to_click_determining(sign_to_write, bet_type, point[1], teams)
        send_msg['msg'] = f'{var.bot_number}: успешно поставил на {result[0]}'
        clickable = is_point_clickable_check(point)
        if clickable:
            pyautogui.click(x=point[0], y=point[1])
            make_bet(send_msg)
        pq.remove(task)
        clear_search_window()
        pyautogui.hotkey(var.start_video_hotkey)
        locker['processing'] = False
        return
    except Exception as e:
        print('error in picture', e)
        pq.remove(task)
        clear_search_window()
        pyautogui.hotkey(var.start_video_hotkey)
        locker['processing'] = False
        return
