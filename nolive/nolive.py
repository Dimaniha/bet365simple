from nolive_Esoccer_draw.nolive_Esoccer_draw import nolive_Esoccer_draw
import re
import var


def nolive(task, send_msg, locker):
    print("na4al nnnnnnnlive")
    for line in range(0, 3):
        if line == 0:
            sport_type = task[1][line]
            if re.search(r'Draw', str(sport_type)):
                print('draw')
                send_msg['msg'] = f'{var.bot_number}: успешно поставил на {sport_type} в нелайве'
                nolive_Esoccer_draw(task[1], send_msg)
                break
