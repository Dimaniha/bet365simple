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



