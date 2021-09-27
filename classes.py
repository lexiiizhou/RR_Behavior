class Event_Node:
    def __init__(self):
        self.prev = None
        self.next = None

    def info(self):
        return self.__dict__


class BonsaiEvent(Event_Node):
    def __init__(self, event):
        self.item = event  # The bonsai_event object itself
        self.event_description = event[0]
        self.timestamp = event[1]
        self.event_code = event[2]
        self.restaurant = event[3]
        self.keyword = event[4]


class Trial(Event_Node):
    """
    Series of bonsai events in the same restaurant stored as
    a doubly linked list
    """

    def __init__(self, first_event, list_of_bonsaievents, index):
        """
        events -- DLL: list of bonsai_event objects
        """
        self.enter = None
        self.initiation = None
        self.tEntry = None
        self.firstEventNode = first_event
        self.termination = None
        self.tone_prob = None
        self.restaurant = None
        self.choice = None
        self.outcome = None  #Quit, reward, or no reward
        self.reward = 0
        self.quit = 0
        self.collection = None
        self.index = index
        self.lapIndex = 0
        self.blockIndex = 0
        self.item = list_of_bonsaievents
