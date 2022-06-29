from .live_Ebasketball.live_Ebasketball import live_Ebasketball, live_Ebasketball_total_halftime, \
    live_Ebasketball_total_fulltime
from .live_Esoccer.live_Esoccer import live_Esoccer, live_Esoccer_total, live_Esoccer_asian_handicap, \
    live_Esoccer_fulltime_result
from .live_football.live_football import live_football
import re


def live(task, send_msg):
    print("na4al live")
    n = 0
    for line in task[1]:
        if line == task[1][0]:
            if re.search(r'Under|Over', str(line)):
                if re.search(r'Halftime', str(line)):
                    live_Ebasketball_total_halftime(task[1], send_msg)
                elif re.search(r'(Fulltime Under)|(Fulltime Over)', str(line)):
                    live_Ebasketball_total_fulltime(task[1], send_msg)
                else:
                    live_Esoccer_total(task[1], send_msg)
                break
            elif re.search(r'Fulltime Result', str(line)):
                print('Fulltime Result')
                live_Esoccer_fulltime_result(task[1], send_msg)
                break
            elif re.search(r'Fulltime Asian Hand', str(line)):
                bet_option_for_msg = line[1:]
                bet_option = line[1:].split('-')[0]
                bet_team = line[1:].split('-', 1)[1]
                print(bet_option_for_msg, bet_option, bet_team, 'hgdsfgsfdgsssssssss')
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
                if re.search(r'Fulltime Asian Hand', str(bet_option)):
                    live_Esoccer_asian_handicap(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)
                else:
                    live_Esoccer(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)
