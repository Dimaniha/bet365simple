import time
import var
import pyautogui
import random
import telebot
from PIL import Image
import masks
import easyocr

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
    point = full_time_result_check_on_page(y_list)
    return point


def full_time_result_check_on_page(y_list):
    if pyautogui.pixelMatchesColor(123, y_list[0], ((56, 216, 120) or (255, 255, 255))):
        point = [371, y_list[1]]
    elif pyautogui.pixelMatchesColor(123, y_list[2], ((56, 216, 120) or (255, 255, 255))):
        point = [371, y_list[3]]
    elif pyautogui.pixelMatchesColor(123, y_list[4], ((56, 216, 120) or (255, 255, 255))):
        pyautogui.press('down')
        time.sleep(1)
        point = [371, y_list[5]]
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


def click_and_bet(point, send_msg, bet_option_for_msg):
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg}'
    pyautogui.click(x=point[0], y=point[1])
    make_bet(send_msg)


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


def screenshot(send_msg):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(var.feedback_screenshot)
    bot.send_photo(var.uid, open(var.feedback_screenshot, 'rb'), caption=send_msg)


def is_point_clickable_check(point):
    pyautogui.moveTo(point[0], point[1])
    time.sleep(0.2)
    if pyautogui.pixelMatchesColor(point[0], point[1], (80, 80, 80)):
        time.sleep(2)
        print('затемнение кнопки')
        is_point_clickable_check(point)
    else:
        return


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


def pixel_match_check():
    x = 350
    for y in range(192, 685):
        pixel = pyautogui.pixel(x, y)
        print(x, y, pixel)
        if pyautogui.pixelMatchesColor(x, y, (56, 216, 120)):
            point = [x, y]
            time.sleep(2)
            return point


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


def text_recognition(screen_path):
    reader = easyocr.Reader(['hu', 'en'])
    result = reader.readtext(screen_path)
    print(result, 'result')
    return result


def get_white_line_range(image_path):
    photo = Image.open(image_path, "r")
    width = photo.size[0]
    height = photo.size[1]
    x = width - 1
    white_line_range = []
    white_line_possible_range = set()
    for y in reversed(range(height)):
        RGB = photo.getpixel((x, y))
        white_line_possible_range.add(RGB)
        if y == height - 100:
            break
    if (240, 240, 240) in white_line_possible_range:  # с линией
        with_line = True
        print('vse matchi')
    else:
        with_line = False
        print('stavka')
    for y in range(height-400, height):
        RGB = photo.getpixel((x, y))
        #print(x, y, RGB)
        if with_line:  # с линией
            if RGB == (240, 240, 240) and photo.getpixel((x, y-1)) != (240, 240, 240):
                white_line_range.append(y)
            elif RGB == (240, 240, 240) and photo.getpixel((x, y+1)) != (240, 240, 240):
                white_line_range.append(y)
                break
        else:  # без линии
            if RGB == (241, 241, 241) and photo.getpixel((x, y-1)) != (241, 241, 241):
                white_line_range.append(y)
            elif RGB == (241, 241, 241) and photo.getpixel((x, y+1)) != (241, 241, 241):
                white_line_range.append(y)
    print(white_line_range)
    return white_line_range, width


