from functions import open_link, is_point_clickable_check, make_bet, screenshot
from .nolive_bet_from_image_functions import *


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
        urls = ['https://www.bet365.com/#/AC/B1/C1/D1002/E72260052/G938/', 'https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/'
                ]
        #8 min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E47578773/G938/'
        #10min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E72260052/G938/'
        #12min = 'https://www.bet365.com/#/AC/B1/C1/D1002/E71755872/G938/'
        teams = [result[2][:len(result[2]) // 2], result[2][len(result[2]) // 2:]]
        team1 = teams[0].split('(')[1].split(')')[0].lower()
        team2 = teams[1].split('(')[1].split(')')[0].lower()
        print(team1, team2)
        team1, team2 = teams_confirmation(team1, team2)
        print(team1, team2)
        #sign_to_write, bet_type = image_sign_to_write_determining(result)
        #print(sign_to_write, bet_type)
        #pq.remove(task)
        #locker['processing'] = False
        #return
        for url in range(len(urls)):
            click = False
            n = 0
            while not click:
                open_link(urls[url])
                time.sleep(3)
                pyautogui.click(372, 304)
                time.sleep(3)
                pyautogui.click(355, 393)
                time.sleep(3)
                sign_to_write = f'({team2}) esports'
                search_on_page(sign_to_write)
                if pyautogui.pixelMatchesColor(142, 707, (242, 186, 199)):
                    next_url = True
                    break
                if n != 0:
                    pyautogui.press('enter', presses=n)
                y, step = [192, 685], 12
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
            try:
                if exitflag:
                    break
            except:
                pass
            try:
                if next_url:
                    continue
            except:
                pass
            if url == len(urls) - 1 and not team1:
                send_msg['msg'] = f'{var.bot_number}: после 3 попыток совпадений не найдено'
                screenshot(send_msg)
                prereturn_actions(pq, task, locker)
                return
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
            screenshot(send_msg)
            prereturn_actions(pq, task, locker)
            return
        pyautogui.click(x=point[0], y=point[1])  # открыл нужную вкладку на странице
        time.sleep(1)
        point = image_point_to_click_determining(sign_to_write, bet_type, point[1], teams)
        send_msg['msg'] = f'{var.bot_number}: успешно поставил на {result[0]}'
        clickable = is_point_clickable_check(point)
        if clickable:
            pyautogui.click(x=point[0], y=point[1])
            make_bet(send_msg)
        prereturn_actions(pq, task, locker)
        return
    except Exception as e:
        print('error in picture', e)
        prereturn_actions(pq, task, locker)
        return
