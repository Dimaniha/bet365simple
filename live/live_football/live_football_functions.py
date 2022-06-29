import re
from functions import screenshot, search_on_page
from classes import Search
import time
import pyautogui
import var
import masks
from nolive.nolive_bet_from_image.nolive_bet_from_image_functions import crop_a_particular_place, text_recognition


def football_half_check(bet_option_for_msg):
    if re.search(r'half', str(bet_option_for_msg)):
        half = True
    else:
        half = False
    return half


def match_goals_check(bet_option_for_msg):
    if re.search(r'Over|Under', str(bet_option_for_msg)):
        match_goals = True
    else:
        match_goals = False
    return match_goals


def football_sign_to_write_determining(bet_option_for_msg, main_line):
    if re.search(r'win', str(bet_option_for_msg)):  # A1
        if re.search(r'win ht', str(bet_option_for_msg)):
            print('half time left')
            sign_to_write = 'half'
        else:
            print('all')
            sign_to_write = 'all'
    elif re.search(r'#A2', str(main_line)):
        print('handicap left')
        sign_to_write = 'asian lines'
    elif re.search(r'#A4', str(main_line)):
        print(' total')
        sign_to_write = 'goals'
    return sign_to_write


def football_bet_point_determining(sign_to_write, left, bet_option, half, match_goals):
    try:
        if sign_to_write == 'half':
            sign_to_write = 'half time result'
            search_on_page(sign_to_write)
            x, y, step, color = 110, [192, 685], 3, (56, 216, 120)
            vs = Search(x, y, step, color)
            point = vs.pixel_match_check_vertical()
            if left:
                point = [178, point[1] + 60]
            else:
                point = [601, point[1] + 60]
            print(sign_to_write)
        elif sign_to_write == 'all':
            sign_to_write = 'fulltime result'
            search_on_page(sign_to_write)
            x, y, step, color = 110, [192, 685], 3, (56, 216, 120)
            vs = Search(x, y, step, color)
            point = vs.pixel_match_check_vertical()
            if left:
                point = [163, point[1] + 60]
            else:
                point = [578, point[1] + 60]
            print(sign_to_write)
        elif sign_to_write == 'goals':
            '''
            for sign_to_write in football_title_types.football_title_types_list:
                pass

                search_on_page(sign_to_write)
                x, y, step = [110, 120], [192, 685], 3
                vs = Search(x[0], y, step)
                point = vs.pixel_match_check_vertical()
                if point:
                    sign_to_write = bet_option[0][:-1].split('(')[1]
                    search_on_page(sign_to_write)
                    vs = Search(x[1], y, step)
                    point = vs.pixel_match_check_vertical()
                    if point:
                        break
                    else:
                        continue
                else:
                    print('matcha ne naideno')
            '''
            if half:
                sign_to_write = 'first half goals'
            else:
                if match_goals:
                    sign_to_write = 'match goals'
                else:
                    sign_to_write = 'alternative match goals'
            print(sign_to_write)
            search_on_page(sign_to_write)
            x, y, step, color = [110, 120], [192, 685], 3, (56, 216, 120)
            vs = Search(x[0], y, step, color)
            point = vs.pixel_match_check_vertical()
            if point:
                sign_to_write = bet_option[0][:-1].split('(')[1]
                search_on_page(sign_to_write)
                vs = Search(x[1], y, step, color)
                point = vs.pixel_match_check_vertical()
            else:
                print('matcha ne naideno')
            time.sleep(0.1)
            ''' do suda '''
            if left:
                point = [248, point[1]]
            else:
                point = [594, point[1]]
        elif sign_to_write == 'asian lines':
            bet_option = bet_option[0][:-1].split('(')[1]
            try:
                if int(bet_option) == 0:
                    bet_option = bet_option + '.0'
                    zero = True
                elif bet_option.isnumeric():
                    bet_option = '+' + bet_option
            except Exception as e:
                print(e)
            print(bet_option)
            if left:
                try:
                    point = asian_lines_complex(bet_option)
                except Exception as e:
                    print('v lifte', e)
            else:
                try:
                    if zero:
                        point = asian_lines_complex(bet_option)
                        point[0] = 420
                except Exception as e:
                    print(e)
                    if re.match(r'-', str(bet_option)):
                        bet_option = re.sub(r'-', '+', str(bet_option))
                    elif re.match(r'\+', str(bet_option)):
                        bet_option = re.sub(r'\+', '-', str(bet_option))
                    point = asian_lines_complex(bet_option)
                    point[0] = 420
        else:
            print('error')
            send_msg = f'{var.bot_number}: что-то пошло не так при попытке определения позиции кнопки'
            screenshot(send_msg)
            return
        print('vozvrashayu point iz football_bet_point_determining')
        return point

    except Exception as e:
        print('football_bet_point_determining', e)


def asian_lines_complex(bet_option):
    try:
        n = 0
        x_4_search, y_4_search, step, color = [193, 200], [376, 686], 3, (56, 216, 120)
        on_line1, point1 = asian_lines_point_determining(bet_option, x_4_search[0], y_4_search, step, color)
        if on_line1:
            return point1
        on_line2, point2 = asian_lines_point_determining(bet_option, x_4_search[1], y_4_search, step, color)
        while not on_line1 or on_line2:
            pyautogui.hotkey('enter')
            on_line1, point1 = asian_lines_point_determining(bet_option, x_4_search[0], y_4_search, step, color)
            if on_line1:
                break
            on_line2, point2 = asian_lines_point_determining(bet_option, x_4_search[1], y_4_search, step, color)
            n += 1
            if n > 6:
                x, y, step, color = 90, [192, 685], 10,
                vs = Search(x, y, step, color)
                point = vs.pixel_match_check_vertical()
                if point[1] < 470:
                    x_4_search, y_4_search, step, color = 165, [376, 686], 3, (56, 216, 120)
                    on_line1, point1 = asian_lines_point_determining(bet_option, x_4_search, y_4_search, step, color)
                    if on_line1:
                        break
                    else:
                        return
                    '''
                    myScreenshot = pyautogui.screenshot()
                    myScreenshot.save(masks.live_football_asian_lines_screenshot)
                    coordinates = [145, 413, 240, 438]
                    crop_a_particular_place(coordinates, masks.live_football_asian_lines_screenshot,
                                            masks.live_football_asian_lines_screenshot_cropped)
                    result = text_recognition(masks.live_football_asian_lines_screenshot_cropped)
                    print(result)
                    '''
                    '''вырезка участка скрина и прогон его через тессеракт и определение цифор'''
        print('vozvrashayu point iz asian_lines_complex')
        if point1:
            return point1
        elif point2:
            return point2
    except Exception as e:
        print('oshibkla v asian_lines_complex', e)


def asian_lines_point_determining(bet_option, x_4_search, y_4_search, step, color):
    try:
        search_on_page(bet_option)
        vs = Search(x_4_search, y_4_search, step, color)
        point = vs.pixel_match_check_vertical()
        if point:
            print('vozvrashayu point iz asian_lines_point_determining')
            return True, point
        else:
            print('vozvrashayu point iz asian_lines_point_determining')
            return False, None
    except Exception as e:
        print('v asian_lines_point_determining', e)
