import re
from functions import open_link, is_point_clickable_check, make_bet, bot, screenshot, search_on_page
from live_football_functions import football_half_check, match_goals_check, football_sign_to_write_determining, \
    football_bet_point_determining
from classes import Search
import var
import pyautogui
import time


def live_football(task, send_msg):
    placed_bets = []
    for line in task:
        if re.match(r'bet365.com', str(line)):
            url = line
            break
    time.sleep(2)
    for line in range(len(task) - 1):
        if re.match(r'#A1|#A2|#A4|#A5', str(task[line])):
            try:
                open_link(url)
                time.sleep(4)
                print('some A')
                bet_option_for_msg = [task[line + 1], task[line + 2]]
                if bet_option_for_msg in placed_bets:
                    continue
                elif task[line] == '#A4':
                    if re.search(r'больше', str(bet_option_for_msg)):
                        left = True
                    elif re.search(r'меньше', str(bet_option_for_msg)):
                        left = False
                    half = football_half_check(bet_option_for_msg)
                    match_goals = match_goals_check(bet_option_for_msg)
                else:
                    if re.search(r'Home', str(bet_option_for_msg)):
                        left = True
                    elif re.search(r'Away', str(bet_option_for_msg)):
                        left = False
                    else:
                        bot.send_message(var.uid, f'{var.bot_number}: Обнаружена неведомая хрень - '
                                                  f'{bet_option_for_msg}')
                        continue
                    half = None
                    match_goals = None
                print(left, 'left')
                print(match_goals)
                sign_to_write = football_sign_to_write_determining(bet_option_for_msg, task[line])
                search_on_page(sign_to_write)
                x_4_search, y_4_search, step = [67, 635], 300, 3
                hs = Search(x_4_search, y_4_search, step)
                point = hs.pixel_match_check_horizontal()
                pyautogui.click(x=point[0], y=point[1])
                time.sleep(1)
                point = football_bet_point_determining(sign_to_write, left, bet_option_for_msg, half, match_goals)
                send_msg['msg'] = ''
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg[0]}'
                clickable = is_point_clickable_check(point)
                if clickable:
                    pyautogui.click(x=point[0], y=point[1])
                    make_bet(send_msg)
                    placed_bets.append(bet_option_for_msg)
                else:
                    continue
            except Exception as e:
                print('osibka v futbole', e)
                send_msg['msg'] = ''
                send_msg['msg'] = f'{var.bot_number}: что-то пошло не так при попытке ставки'
                screenshot(send_msg)
                continue
