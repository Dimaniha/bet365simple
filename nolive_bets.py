import re
from functions import *


def nolive_Esoccer_draw(task, send_msg):
    n = 0
    for line in task:
        if re.search(r'https', str(line)):
            url = line
        elif re.search(r'\svs\s', str(line)):
            if n == 0:
                teams = line[1:].split('vs')
                n += 1
    open_link(url)
    team_search_on_page(teams)
    coordinates = [770, 702, 780, 713]
    crop_a_particular_place(coordinates, masks.nolive_draws_page_screen, masks.nolive_quantity_matches_found)
    quantity_matches_found = text_recognition(masks.nolive_quantity_matches_found)
    print(quantity_matches_found)
    for iter in range(quantity_matches_found):
        try:
            team_search_on_page(teams)
            coordinates = [232, 227, 537, 685]
            crop_a_particular_place(coordinates, masks.nolive_draws_page_screen, masks.nolive_draws_teams)
            teams_on_page = text_recognition(masks.nolive_draws_teams)
            for i in range(len(teams_on_page) - 1):
                if re.search(fr'{teams[0]}', str(teams_on_page[i][1].lower().strip())) and \
                        re.search(rf'{teams[1]}', str(teams_on_page[i+1][1].lower().strip())):
                    team1_coords = teams_on_page[i][0][0]
                    print('nashelk')
                    break
            print(team1_coords)
        except UnboundLocalError as e:
            print('unbound', e)
            continue
        else:
            break
    pyautogui.click(x=team1_coords[0], y=team1_coords[1])
    time.sleep(1)
    position = title_teams_len_check(teams)
    print('position', position)
    point = full_time_result_check(position)
    print(point)
    is_point_clickable_check(point)
    print('clickable???', )
    pyautogui.click(x=point[0], y=point[1])
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {task[0][1:]}'
    make_bet(send_msg)


def nolive_table_tennis(url, bet_option, sport_type, send_msg):
    option = bet_option.split()[0]
    send_msg['msg'] = f'{var.bot_number}: успешно поставил на {sport_type} - {bet_option}'
    open_link(url)
    if option == 'o':
        point = [614, 451]
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(2)
        make_bet(send_msg)
    elif option == 'u':
        point = [878, 451]
        pyautogui.click(x=point[0], y=point[1])
        time.sleep(2)
        make_bet(send_msg)


def nolive_soccer(url, bet_option, sport_type):
    pass


def nolive_ice_hockey(url, bet_option, sport_type):
    pass


def nolive_basketball(url, bet_option, sport_type):
    pass