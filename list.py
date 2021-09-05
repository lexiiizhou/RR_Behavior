import pandas as pd
import list as ls
import copy


class DoublyLinkedList:
    """A doubly linked list data structure"""

    def __init__(self):
        self.sentinel = ls.Event_Node()
        self.sentinel.next = None
        self.sentinel.prev = None
        self.size = 0

    def write_dataFrame(self):
        assert self.sentinel.next is not None
        n = self.sentinel.next
        list_of_objects = []
        while n is not None:
            list_of_objects.append(n.current)
            n = n.next
        dataFrame = pd.DataFrame([obj.__dict__ for obj in list_of_objects])
        dataFrame = dataFrame.drop(columns=['item', 'prev', 'next'])
        return dataFrame

    def add_first(self, item):
        new_item = copy.deepcopy(item)
        new_item.next = None
        new_item.prev = None
        self.sentinel.next = new_item
        self.sentinel.prev = new_item
        self.size += 1

    def add_to_end(self, item):
        if self.size == 0:
            self.add_first(item)
            return
        new_last = copy.deepcopy(item)
        new_last.next = None
        new_last.prev = None
        self.sentinel.prev.next = new_last
        self.sentinel.prev = new_last
        self.size += 1

    def add_to_start(self, item):
        if size == 0:
            self.add_first(item)
            return
        new_last = copy.deepcopy(item)
        new_last.next = None
        new_last.prev = None
        self.sentinel.next.prev = new_last
        self.sentinel.next = new_last
        self.size += 1
