﻿from functions import *
from classes import PriorityQueue
from multiprocessing import Process
from live.live import live
import multiprocessing
import datetime


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
        pyautogui.click(x=909, y=126)
        send_msg = f'{var.bot_number}: Скриншот истории.'
        screenshot(send_msg)

    @bot.channel_post_handler(commands=['new'])
    @bot.message_handler(commands=['new'])
    @busy_check
    def unsettled_screen(message):
        pyautogui.click(x=909, y=126)
        time.sleep(0.1)
        pyautogui.click(x=741, y=149)
        send_msg = f'{var.bot_number}: Скриншот нерасчитанных.'
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
            p.add_new(answer, pq, priority=0)
        except Exception as e:
            print("error!!", e)

    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("error while polling", e)


def start_process(pq, send_msg):
    while True:
        if len(pq) > 0:
            try:
                print(pq)
                print(len(pq))
                task = pq[0]
                pyautogui.hotkey(var.start_video_hotkey)
                live(task, send_msg)
                pq.remove(task)
                pyautogui.hotkey(var.start_video_hotkey)
            except Exception as e:
                print('exception in main circle', e)


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    manager = multiprocessing.Manager()
    send_msg = manager.dict()
    send_msg['msg'] = ' '
    locker = manager.dict()
    locker['locked'] = False
    pq = manager.list()
    start_proc = Process(target=start, args=(pq, locker, send_msg))
    work_proc = Process(target=start_process, args=(pq, send_msg))
    start_proc.start()
    work_proc.start()
    while True:
        if not start_proc.is_alive():
            print("terminate")
            start_proc.terminate()
            start_proc = Process(target=start, args=(pq, locker, send_msg))
            start_proc.start()
