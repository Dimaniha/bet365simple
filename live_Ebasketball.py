import re
from functions import open_link, bot, teams_icon_cutter, screenshot, one_click_bet_check, scrollbar_position_check, \
    point_determining
import abandoned_boys
import var
import pyautogui
import time


def live_Ebasketball(teams, bet_option, bet_team, bet_option_for_msg, send_msg):
    if re.search(r'Fulltime Asian Hand', str(bet_option)):
        print("hand")
        bet_name = re.split(r"-|\+", str(bet_team))[0]
        if bet_name.strip() in abandoned_boys.ebasket_Fulltime_Asian_Hand_list:
            bot.send_message(var.uid, f'{var.bot_number}: Фора на {bet_name} - ставку пропускаю')
            return
        teams = teams_icon_cutter(teams)
        teams_len = len(teams)
        print(teams)
        pyautogui.hotkey('f5')
        time.sleep(2)
        match = open_link(bet_name)
        if not match:
            return
        scrollbar_position_check()
        one_click_bet_check()
        point = point_determining(teams_len, bet_name, teams, bet_option_for_msg, send_msg)
        if not pyautogui.pixelMatchesColor(891, 177, (37, 62, 91)):
            pyautogui.click(x=point[0], y=point[1])
            time.sleep(3)
            one_click_bet_check()
        pyautogui.click(x=point[0], y=point[1])
        screenshot(send_msg['msg'])
