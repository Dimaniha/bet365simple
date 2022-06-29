import pyautogui
import time


class PriorityQueue:
    def add_new(self, task, queue, priority=0):
        item = [priority, task]
        queue.append(item)
        last_item = len(queue) - 1
        if last_item == 0:
            return queue
        else:
            for i in range(0, last_item):
                for x in range(0, last_item - i):
                    if queue[x][0] > queue[x+1][0]:
                        queue[x], queue[x+1] = queue[x+1], queue[x]
            return queue


class Search:
    def __init__(self, x, y, step, color):
        self.x = x
        self.y = y
        self.step = step
        self.color = color

    def pixel_match_check_horizontal(self):
        for x_ in range(self.x[0], self.x[1], self.step):
            pyautogui.moveTo(x_, self.y)
            pixel = pyautogui.pixel(x_, self.y)
            print(x_, self.y, pixel)
            if pyautogui.pixelMatchesColor(x_, self.y, self.color): #(56, 216, 120)
                point = [x_, self.y]
                time.sleep(2)
                return point

    def pixel_match_check_vertical(self):
        for y_ in range(self.y[0], self.y[1], self.step):
            pyautogui.moveTo(self.x, y_)
            pixel = pyautogui.pixel(self.x, y_)
            print(self.x, y_, pixel)
            if pyautogui.pixelMatchesColor(self.x, y_, self.color):
                point = [self.x, y_]
                time.sleep(2)
                return point
