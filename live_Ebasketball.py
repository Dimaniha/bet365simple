import re
from functions import open_link, bot, teams_icon_cutter, screenshot, one_click_bet_check, scrollbar_position_check
import abandoned_boys
import var
import pyautogui


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
        for word in range(0, teams_len):
            if re.match(rf'{bet_name.strip().lower()}', str(teams[word].strip().lower())):
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {bet_option_for_msg}'
                if word == 0:  # column 1
                    print("column 1")
                    point = [272, 387]
                    break
                else:  # column 2
                    print("column 2")
                    point = [592, 387]
                    break
        pyautogui.click(x=point[0], y=point[1])
        screenshot(send_msg['msg'])
