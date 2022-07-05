from live_Ebasketball import live_Ebasketball
import re


def live(task, send_msg):
    print("na4al live")
    n = 0
    for line in task[1]:
        if line == task[1][0]:
            if re.search(r'Fulltime Asian Hand', str(line)):
                bet_option_for_msg = line[1:]
                bet_option = line[1:].split('-')[0]
                bet_team = line[1:].split('-', 1)[1]
                print(bet_option_for_msg, bet_option, bet_team, 'hgdsfgsfdgsssssssss')
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line
                n += 1
        elif re.search(r'https', str(line)):
            if re.search(r'🏀', str(teams)):
                print("basket")
                live_Ebasketball(teams, bet_option, bet_team, bet_option_for_msg, send_msg)
