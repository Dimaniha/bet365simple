from nolive_bets import *


def nolive(task, send_msg):
    for line in range(0, 3):
        if line == 0:
            sport_type = task[1][line]
            if re.search(r'Draw', str(sport_type)):
                print('draw')
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {sport_type} в нелайве'
                nolive_Esoccer_draw(task[1], send_msg)
                break
        elif line == 1:
            url = task[1][line]
        elif line == 2:
            bet_option = task[1][line]
    if re.search(r'tt', str(sport_type)):
        nolive_table_tennis(url, bet_option, sport_type, send_msg)
    elif re.search(r'soccer', str(sport_type)):
        nolive_soccer(url, bet_option, sport_type)
    elif re.search(r'ice hockey', str(sport_type)):
        nolive_ice_hockey(url, bet_option, sport_type)
    elif re.search(r'basketball', str(sport_type)):
        nolive_basketball(url, bet_option, sport_type)