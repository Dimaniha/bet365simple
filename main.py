from live import *
from nolive import *
from classes import PriorityQueue
from multiprocessing import Process
import multiprocessing


pyautogui.FAILSAFE = False
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

    @bot.channel_post_handler(func=lambda message: True, content_types=['photo'])
    @bot.message_handler(func=lambda message: True, content_types=['photo'])
    def get_picture_prediction(message):
        print('nasd')
        capt = message.caption
        if re.search(r'bot', str(capt)):
            print('neet')
            return
        else:
            print(capt)
            raw = message.photo[2].file_id
            path = 'bet_screens/' + raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            print(path)
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            p.add_new(path, pq, priority=2)

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
                elif re.search(r'bet365.dk', str(line)):
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
        if len(pq) > 0 and locker['locked'] is False:
            print(pq)
            print(len(pq))
            try:
                #pyautogui.hotkey(var.start_video_hotkey)
                remain_window_check()
                task = pq[0]
                if re.search(r'#/IP/EV', str(task)):
                    print("nashel live")
                    live(task, send_msg)
                else:
                    print("nashel nolive")
                    nolive(task, send_msg)
                pq.remove(task)
                #pyautogui.hotkey(var.start_video_hotkey)
            except Exception as e:
                print('эксепшон', e)
                pq.remove(task)


def location_():  # определение коорд указателя для тестов
    time.sleep(7)
    # pyautogui.moveTo(612, 462)
    n = pyautogui.position()
    print(n)
    pix = pyautogui.pixel(n[0], n[1])
    print(pix)
    time.sleep(40)


if __name__ == '__main__':
    #location_()
    start_time = datetime.datetime.now()
    manager = multiprocessing.Manager()
    send_msg = manager.dict()
    send_msg['msg'] = ' '
    locker = manager.dict()
    locker['locked'] = False
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