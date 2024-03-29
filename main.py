﻿from functions import *
from classes import PriorityQueue
from multiprocessing import Process
from live.live import live
from nolive.nolive import nolive
from nolive.nolive_bet_from_image.nolive_bet_from_image import nolive_bet_from_image
import multiprocessing
import re
import datetime
import masks


p = PriorityQueue()


def start(pq, locker, send_msg):
    def busy_check(f):
        def wrapper(message):
            if len(pq) == 0 and locker['locked'] is False:
                locker['locked'] = True
                result = f(message)
                locker['locked'] = False
                return result
            else:
                bot.send_message(var.uid, f'{var.bot_number}: Я пока занят, напишите позже.')
                return
        return wrapper

    @bot.channel_post_handler(commands=['screen'])
    @bot.message_handler(commands=['screen'])
    @busy_check
    def make_screen(message):
        send_msg = f'{var.bot_number}: Скриншот текущей страницы.'
        screenshot(send_msg)

    @bot.channel_post_handler(commands=['old'])
    @bot.message_handler(commands=['old'])
    @busy_check
    def settled_screen(message):
        remain_window_check()
        pyautogui.click(x=597, y=155)
        time.sleep(1)
        pyautogui.click(x=238, y=205)
        send_msg = f'{var.bot_number}: Скриншот My bets - Settled.'
        screenshot(send_msg)

    @bot.channel_post_handler(commands=['new'])
    @bot.message_handler(commands=['new'])
    @busy_check
    def unsettled_screen(message):
        remain_window_check()
        pyautogui.click(x=597, y=155)
        time.sleep(1)
        pyautogui.click(x=176, y=206)
        send_msg = f'{var.bot_number}: Скриншот My bets - Unsettled.'
        screenshot(send_msg)

    @bot.edited_message_handler(func=lambda message: True, content_types=['text'])
    @bot.edited_channel_post_handler(func=lambda message: True, content_types=['text'])
    def change_msg(message):
        answer = message.text.split('\n')
        strings_to_add = answer[-2:]
        text = send_msg['msg'] + '\n'
        for i in strings_to_add:
            text = text + str(i) + '\n'
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id + 1, caption=text)

    @bot.channel_post_handler(func=lambda message: True, content_types=['text'])
    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def get_message(message):
        try:
            answer = message.text
            print(answer)
            answer = answer.split('\n')
            for line in answer:
                if re.search(r'www.bet365.com', str(line)):
                    if re.search(r'#/IP/EV', str(line)):  # live
                        print("live")
                        p.add_new(answer, pq, priority=0)
                    else:  # nolive
                        print("nolive")
                        p.add_new(answer, pq, priority=1)
                    break
                elif re.search(r'https://', str(line)) and not re.search(r'www.bet365.com', str(line)):
                    bot.send_message(var.uid, f'{var.bot_number}: Линия другого букмекера. Ставку пропускаю.')
                    break
                elif re.match(r'bet365.com', str(line)):
                    p.add_new(answer, pq, priority=0)
                    break

        except Exception as e:
            print("error!!", e)

    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("error while polling", e)


def start_process(pq, locker, send_msg):
    while True:
        if len(pq) > 0 and locker['page_waiting'] is False:
            try:
                #remain_window_check()
                if locker['locked'] is False and locker['processing'] is False and pq[0][0] != 2:
                    print(pq)
                    print(len(pq))
                    try:
                        task = pq[0]
                        pyautogui.hotkey(var.start_video_hotkey)
                        if re.search(r'#/IP/EV', str(task)):
                            print("nashel live")
                            live(task, send_msg)
                        elif task[0] == 1:
                            print("nashel nolive")
                            nolive(task, send_msg, locker)
                        pq.remove(task)
                        if len(pq) == 0:
                            pyautogui.click(x=418, y=155)
                        clear_search_window()
                        pyautogui.hotkey(var.start_video_hotkey)
                    except Exception as e:
                        print('эксепшон', e)
                        pq.remove(task)
                        clear_search_window()
                        if len(pq) == 0:
                            pyautogui.click(x=418, y=155)
                        pyautogui.hotkey(var.start_video_hotkey)
                elif locker['locked'] is False and locker['processing'] is False and pq[0][0] == 2:
                    print("nashel stavku s kartinki")
                    remain_window_check()
                    task = pq[0]
                    bet_from_image_proc = Process(target=nolive_bet_from_image, args=(task, send_msg, locker, pq))
                    bet_from_image_proc.start()
                    locker['processing'] = True
            except Exception as e:
                print('exception in main circle', e)
        elif locker['page_waiting'] is True and len(pq) > 1 and pq[0][0] == 0:
            print('bolshe 1 terminate')
            bet_from_image_proc.terminate()
            locker['page_waiting'] = False
            locker['processing'] = False
        elif locker['processing'] is True and locker['page_waiting'] is False and len(pq) > 1 and pq[0][0] == 0:
            print('bolshe 1')
            bet_from_image_proc.terminate()
            locker['processing'] = False


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    manager = multiprocessing.Manager()
    send_msg = manager.dict()
    send_msg['msg'] = ' '
    locker = manager.dict()
    locker['locked'] = False
    locker['page_waiting'] = False
    locker['processing'] = False
    pq = manager.list()
    start_proc = Process(target=start, args=(pq, locker, send_msg))
    work_proc = Process(target=start_process, args=(pq, locker, send_msg))
    start_proc.start()
    work_proc.start()
    while True:
        if (datetime.datetime.now() - start_time).total_seconds() // 1800.0 >= 1 and len(pq) == 0:
            locker['locked'] = True
            check_login()
            start_time = datetime.datetime.now()
            locker['locked'] = False
        elif not start_proc.is_alive():
            print("terminate")
            start_proc.terminate()
            start_proc = Process(target=start, args=(pq, locker, send_msg))
            start_proc.start()
