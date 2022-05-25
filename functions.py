import time
import var
import pyautogui
import random
import telebot
from PIL import Image, ImageEnhance
import pytesseract
import masks
import re
from classes import Search
#import football_title_types
import tips_4_screenshots_bets


pytesseract.pytesseract.tesseract_cmd = var.tesseract_cmd
pyautogui.FAILSAFE = False
bot = telebot.TeleBot(var.API_TOKEN)

def remain_window_check():
    pyautogui.moveTo(622, 339)
    time.sleep(random.random())
    if pyautogui.pixelMatchesColor(622, 339, (22, 131, 97)):
        pyautogui.click()


def full_time_result_check(position):
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.press('backspace')
    pyautogui.write('fulltime result')
    print('poisk full...')
    time.sleep(0.1)
    if position:
        y_list = [621, 660, 379, 428, 669, 652]
    else:
        y_list = [591, 630, 349, 398, 639, 622]
    x_list = [123, 371]
    point = full_time_result_check_on_page(x_list, y_list)
    return point


def full_time_result_check_on_page(x_list, y_list):
    if pyautogui.pixelMatchesColor(x_list[0], y_list[0], ((56, 216, 120) or (255, 255, 255))):
        point = [x_list[1], y_list[1]]
    elif pyautogui.pixelMatchesColor(x_list[0], y_list[2], ((56, 216, 120) or (255, 255, 255))):
        point = [x_list[1], y_list[3]]
    elif pyautogui.pixelMatchesColor(x_list[0], y_list[4], ((56, 216, 120) or (255, 255, 255))):
        pyautogui.press('down')
        time.sleep(1)
        point = [x_list[1], y_list[5]]
    return point


def total_check():
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.press('backspace')
    sign_to_write = 'over'
    pyautogui.write(sign_to_write)
    print('poisk...')
    time.sleep(0.2)
    pyautogui.moveTo(663, 208)
    time.sleep(0.2)
    if not pyautogui.pixelMatchesColor(663, 208, (103, 103, 103)):
        pyautogui.click(x=663, y=208, button='left', clicks=5, interval=0.5)
        print('vernulos false')
        return False
    else:
        print('na meste')
        return True


def Both_Teams_to_Score_check(word, y_check):
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.write('both teams')
    time.sleep(0.3)
    if pyautogui.pixelMatchesColor(100, y_check, ((56, 216, 120) or (255, 255, 255))):
        print('both')
        if word == 0:
            y = y_check + 121
        else:
            y = y_check + 236
        return y
    else:
        if not pyautogui.pixelMatchesColor(663, 208, (103, 103, 103)):
            pyautogui.click(x=663, y=208, button='left', clicks=5, interval=0.5)
            if word == 0:
                y = y_check + 70
            else:
                y = y_check + 190
            return y
        else:
            if word == 0:
                y = y_check + 70
            else:
                y = y_check + 190
            return y


def open_link(url):
    pyautogui.click(x=455, y=52)  # вставить ссылку
    time.sleep(random.random())
    pyautogui.press('backspace')
    time.sleep(random.random())
    pyautogui.write(url)
    time.sleep(random.random())
    pyautogui.press('enter')
    time.sleep(2.5)
    return


def check_login():
    pyautogui.click(x=490, y=154)
    pyautogui.hotkey('f5')
    time.sleep(10)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('log in')
    if pyautogui.pixelMatchesColor(980, 160, (56, 216, 120)):
        print('отлогинилось((')
        bot.send_message(var.uid, f'{var.bot_number}: лк вылетел, пытаюсь залогиниться, но лучше проверить')
        pyautogui.click(x=980, y=160)
        time.sleep(random.random())
        pyautogui.click(x=600, y=291)
        pyautogui.write(var.paswd)
        time.sleep(random.random())
        pyautogui.click(x=621, y=350)
        time.sleep(8)
        send_msg = f'{var.bot_number}: я попытался залогиниться, надо проверить скрин'
        screenshot(send_msg)
        print('залогинилось')
        print('false')
        return False
    else:
        print('True')
        return True


def make_bet(send_msg):
    time.sleep(0.5)
    pyautogui.click(x=697, y=623)
    time.sleep(1)
    n = 0
    while True:
        if not pyautogui.pixelMatchesColor(655, 622, (240, 240, 240)):
            pyautogui.click(x=697, y=623)
            print('cliknul')
            time.sleep(1)
            n += 1
            if n == 60:
                print('минута прошла')
                result = check_login()
                if result:
                    send_msg['msg'] = f'{var.bot_number}: лк залогинен, но что-то пошло не так. ' \
                                      f'Возможно ставка менялась слишком много раз'
                    screenshot(send_msg['msg'])
                    return
                else:
                    return
        else:
            break
    time.sleep(7)
    screenshot(send_msg['msg'])
    time.sleep(random.random())
    pyautogui.click(x=705, y=445)
    clear_search_window()


def clear_search_window():
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.press('backspace')


def screenshot(send_msg):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(var.feedback_screenshot)
    bot.send_photo(var.uid, open(var.feedback_screenshot, 'rb'), caption=send_msg)


def is_point_clickable_check(point):
    pyautogui.moveTo(point[0], point[1])
    time.sleep(0.2)
    n = 0
    while True:
        if pyautogui.pixelMatchesColor(point[0], point[1], (80, 80, 80)):
            time.sleep(2)
            print('затемнение кнопки')
            time.sleep(1)
            n += 1
            if n == 20:
                print('20 сек прошло')
                send_msg = f'{var.bot_number}: Кнопка ставки была неактивна 20 секунд'
                screenshot(send_msg)
                return False
        else:
            return True


def title_teams_len_check(teams):
    sign_to_write = f'({teams[1].strip()}) esports'
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(sign_to_write)
    time.sleep(0.5)
    if pyautogui.pixelMatchesColor(84, 269, (((56, 216, 120) or (255, 255, 255)))): #2 строки
        position = True
    elif pyautogui.pixelMatchesColor(220, 269, (((56, 216, 120) or (255, 255, 255)))): #2 строки
        position = True
    elif pyautogui.pixelMatchesColor(320, 269, (((56, 216, 120) or (255, 255, 255)))): #2 строки
        position = True
    elif pyautogui.pixelMatchesColor(411, 269, (((56, 216, 120) or (255, 255, 255)))): #2 строки
        position = True
    else: # 1строка
        position = False
    return position


def search_on_page(sign_to_write):
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write(sign_to_write)
    time.sleep(0.3)


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


def crop_a_particular_place(coordinates, image_path_open, croped_image_path_save):
    im = Image.open(image_path_open)
    left = coordinates[0]
    top = coordinates[1]
    right = coordinates[2]
    bottom = coordinates[3]
    im = im.crop((left, top, right, bottom))
    im.save(croped_image_path_save)


def get_white_line_range(image_path):
    photo = Image.open(image_path, "r")
    width = photo.size[0]
    height = photo.size[1]
    x = width - 1
    white_line_range = []
    for y in range(height-400, height):
        RGB = photo.getpixel((x, y))
        #print(x, y, RGB)
        if RGB == (240, 240, 240):
            white_line_range.append(y)
            break
        elif RGB == (241, 241, 241):
            white_line_range.append(y)
            break
        elif RGB == (235, 235, 235):
            white_line_range.append(y)
            break
    for y in reversed(range(height)):
        RGB = photo.getpixel((x, y))
        #print(x, y, RGB)
        if RGB == (240, 240, 240):
            white_line_range.append(y)
            break
        elif RGB == (241, 241, 241):
            white_line_range.append(y)
            break
    print(white_line_range)
    return white_line_range, width


def text_recognition(screen_path):
    img = Image.open(screen_path)
    enhancer1 = ImageEnhance.Sharpness(img)
    enhancer2 = ImageEnhance.Contrast(img)
    img_edit = enhancer1.enhance(20.0)
    img_edit = enhancer2.enhance(1.5)
    img_edit.save("edited_image.png")
    result = pytesseract.image_to_string(img_edit)
    print(result.split('\n'))
    return result.split('\n')


def spaces_delete(result):
    result_sorted = []
    for i in result:
        if i == '':
            continue
        else:
            result_sorted.append(i)
    return result_sorted


def image_sign_to_write_determining(result):
    bet_type = result[0]
    for x in tips_4_screenshots_bets.asian_lines_tips:
        if re.search(rf'{x}', str(result[1])):
            print('handicap')
            bet_string = bet_type.split('(')
            if re.search(r'\(', str(bet_string[1])):
                bet_type = bet_string[1].split('(')[1].split(')')[0].lower()
            else:
                bet_type = bet_type.split('(')[1].split(')')[0].lower()
            bet_type = team_tips_check(bet_type)
            sign_to_write = 'asian lines'
            break
    for x in tips_4_screenshots_bets.full_time_result_tips:
        if re.search(rf'{x}', str(result[1])):
            print('pobeda fultime')
            if re.search(r'draw|Draw', str(bet_type)):
                bet_type = 'draw'
            else:
                bet_type = bet_type.split('(')[1].split(')')[0].lower()
                bet_type = team_tips_check(bet_type)
            sign_to_write = 'all'
            break
    for x in tips_4_screenshots_bets.goal_line_tips:
        if re.search(rf'{x}', str(result[1])):
            print('Goal Line')
            if re.search(r'felett|over', str(bet_type.lower())):
                bet_type = 'over'
            elif re.search(r'alatt|under', str(bet_type.lower())):
                bet_type = 'under'
            sign_to_write = 'goals'
            break
    return sign_to_write, bet_type


def team_tips_check(team1):
    for team in tips_4_screenshots_bets.nicknames:
        if team1 == team:
            team1 = tips_4_screenshots_bets.nicknames[team]
    return team1


def match_page_clickable_check(locker, n):
    sign_to_write = 'esoccer'
    search_on_page(sign_to_write)
    time.sleep(0.1)
    if pyautogui.pixelMatchesColor(273, 237, (((56, 216, 120) or (255, 255, 255)))):
        locker['page_waiting'] = True
        print('knopka neaktivna')
        time.sleep(10)
        n = 0
        return False, n
    else:
        locker['page_waiting'] = False
        return True, n


def tab_check(sign_to_write):
    search_on_page(sign_to_write)
    x, y, step = [256, 590], [290, 322, 331], 10
    for y_ in y:
        if y_ == 331:
            x = [67, 375]
        hs = Search(x, y_, step)
        point = hs.pixel_match_check_horizontal()
        if point:
            return point
        else:
            return None


def image_point_to_click_determining(sign_to_write, bet_type, y, teams):
    if bet_type == 'under': # right
        x_goals = [802, 477]
    elif bet_type == 'over': # left
        x_goals = [492, 247]
    elif bet_type == 'draw':
        x_all = [640, 377]
    else:
        for word in range(len(teams)):
            if re.search(rf'{bet_type}', str(teams[word])):
                if word == 0:
                    x_all = [436, 185]
                    x_lines = [436, 130]
                else:
                    x_all = [952, 600]
                    x_lines = [952, 420]
    print(bet_type)
    if y == 290:
        if sign_to_write == 'all':
            point = [x_all[0], 394]
        elif sign_to_write == 'asian lines':
            point = [x_lines[0], 416]
        elif sign_to_write == 'goals':
            point = [x_goals[0], 416]
    elif y == 322:
        if sign_to_write == 'all':
            point = [x_all[0], 422]
        elif sign_to_write == 'asian lines':
            point = [x_lines[0], 450]
        elif sign_to_write == 'goals':
            point = [x_goals[0], 447]
    elif y == 331:
        if sign_to_write == 'all':
            x_list = [262, 654]
            y_list = [337, 386, 369, 418]
            point = full_time_result_check_on_page(x_list, y_list)
            point = [x_all[1], point[1]]
        elif sign_to_write == 'asian lines': # x  1 = 94  2 = 412
            point = [x_lines[1], 450]
        elif sign_to_write == 'goals':
            sign_to_write = 'match goals'
            search_on_page(sign_to_write)
            x, y, step = 110, [192, 685], 3
            vs = Search(x, y, step)
            point = vs.pixel_match_check_vertical()
            point = [x_goals[1], point[1]+80]
    return point


def football_sign_to_write_determining(bet_option_for_msg, main_line):
    if re.search(r'win', str(bet_option_for_msg)):  #A1
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


def football_bet_point_determining(sign_to_write, left, bet_option, half, match_goals):
    try:
        if sign_to_write == 'half':
            sign_to_write = 'half time result'
            search_on_page(sign_to_write)
            x, y, step = 110, [192, 685], 3
            vs = Search(x, y, step)
            point = vs.pixel_match_check_vertical()
            if left:
                point = [178, point[1] + 60]
            else:
                point = [601, point[1] + 60]
            print(sign_to_write)
        elif sign_to_write == 'all':
            sign_to_write = 'fulltime result'
            search_on_page(sign_to_write)
            x, y, step = 110, [192, 685], 3
            vs = Search(x, y, step)
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
            x, y, step = [110, 120], [192, 685], 3
            vs = Search(x[0], y, step)
            point = vs.pixel_match_check_vertical()
            if point:
                sign_to_write = bet_option[0][:-1].split('(')[1]
                search_on_page(sign_to_write)
                vs = Search(x[1], y, step)
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
        x_4_search, y_4_search, step = [193, 200], [376, 686], 3
        on_line1, point1 = asian_lines_point_determining(bet_option, x_4_search[0], y_4_search, step)
        if on_line1:
            return point1
        on_line2, point2 = asian_lines_point_determining(bet_option, x_4_search[1], y_4_search, step)
        while not on_line1 or on_line2 and n < 6:
            pyautogui.hotkey('enter')
            on_line1, point1 = asian_lines_point_determining(bet_option, x_4_search[0], y_4_search, step)
            if on_line1:
                break
            on_line2, point2 = asian_lines_point_determining(bet_option, x_4_search[1], y_4_search, step)
            n += 1
        print('vozvrashayu point iz asian_lines_complex')
        if point1:
            return point1
        elif point2:
            return point2
    except Exception as e:
        print('oshibkla v asian_lines_complex', e)


def asian_lines_point_determining(bet_option, x_4_search, y_4_search, step):
    try:
        search_on_page(bet_option)
        vs = Search(x_4_search, y_4_search, step)
        point = vs.pixel_match_check_vertical()
        if point:
            print('vozvrashayu point iz asian_lines_point_determining')
            return True, point
        else:
            print('vozvrashayu point iz asian_lines_point_determining')
            return False, None
    except Exception as e:
        print('v asian_lines_point_determining', e)
