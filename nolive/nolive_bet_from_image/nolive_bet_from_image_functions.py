from functions import full_time_result_check_on_page, search_on_page
from PIL import Image, ImageEnhance
import pytesseract
import var
import masks
from .tips_4_screenshots_bets import *
import re
import pyautogui
import time
from classes import Search


pyautogui.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = var.tesseract_cmd


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
    img_edit.save(masks.nolive_white_line)
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
