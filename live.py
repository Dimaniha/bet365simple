from live_bets import *


def live(task, send_msg):
    print("na4al live")
    n = 0
    for line in task[1]:
        if line == task[1][0]:
            if re.search(r'Under|Over', str(line)):
                if re.search(r'Halftime', str(line)):
                    live_basketball_total(task[1], send_msg)
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
        elif re.search(r'bet365.dk', str(line)):
            url = re.sub(r'bet365.dk', 'bet365.com', str(line))
            open_link(url)
            live_football(task[1], send_msg)
            break
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line
                n += 1
        elif re.search(r'https', str(line)):
            url = line
            if re.search(r'🏓', str(teams)):
                live_table_tennis(teams, bet_option, bet_team, url)
            elif re.search(r'🏀', str(teams)):
                print("basket")
                live_basketball(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)
            elif re.search(r'⚽', str(teams)):
                print("footba")
                live_Esoccer(teams, bet_option, bet_team, url, bet_option_for_msg, send_msg)