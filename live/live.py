from .live_Ebasketball.live_Ebasketball import live_Ebasketball, live_Ebasketball_total
from .live_Esoccer.live_Esoccer import live_Esoccer, live_Esoccer_draw, live_Esoccer_total
from .live_football.live_football import live_football
import re


def live(task, send_msg):
    print("na4al live")
    n = 0
    for line in task[1]:
        if line == task[1][0]:
            if re.search(r'Under|Over', str(line)):
                if re.search(r'Halftime', str(line)):
                    live_Ebasketball_total(task[1], send_msg)
                else:
                    live_Esoccer_total(task[1], send_msg)
                break
            elif re.search(r'Draw', str(line)):
                print('draw')
                live_Esoccer_draw(task[1], send_msg)
                break
            elif re.search(r'Fulltime Asian Hand', str(line)):
                bet_option_for_msg = line[1:]
                bet_option = line[1:].split('-')[0]
                bet_team = line[1:].split('-', 1)[1]
        elif re.match(r'bet365.com/', str(line)):
            print('some A')
            live_football(task[1], send_msg)
            break
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line
                n += 1
        elif re.search(r'https', str(line)):
            url = line
            if re.search(r'🏀', str(teams)):
                print("basket")
                live_Ebasketball(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)
            elif re.search(r'⚽', str(teams)):
                print("footba")
                live_Esoccer(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)
