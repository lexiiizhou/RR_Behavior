class Event_Node:
    def __init__(self):
        self.current = None
        self.prev = None
        self.next = None

class BonsaiEvent(Event_Node):
    def __init__(self, event):
        self.item = event  # The bonsai_event object itself
        self.event_description = event[0]
        self.timestamp = event[1]
        self.event_code = event[2]
        self.restaurant = event[3]
        self.keyword = event[4]
        self.current = self


class Trial(Event_Node):
    """
    Series of bonsai events in the same restaurant stored as
    a doubly linked list
    """

    def __init__(self, dll_of_bonsaievents, index):
        """
        events -- DLL: list of bonsai_event objects
        """
        self.valid = False  # True: Valid Trial
        self.tone_prob = None
        self.restaurant = None
        self.choice = None
        self.negotiation = None
        self.collection = None
        self.index = index
        self.item = dll_of_bonsaievents
        self.current = self


class Lap(Event_Node):
    """A doubly linked list of trials"""

    def __init__(self, dll_of_trials, index):
        self.index = index
        self.total_trial_count = dll_of_trials.size
        self.valid_trial_count = None
        self.item = dll_of_trials
        self.current = self


class Block(Event_Node):
    """A doubly linked list of laps"""
    def __init__(self, dll_of_laps, index):
        self.index = index
        self.total_lap_count = dll_of_laps.size
        self.item = dll_of_laps
        self.current = self
        self.duration = None

class Session:
    """A doubly linked list of laps"""

    def __init__(self, dll_of_laps):
        self.lap_count = dll_of_laps.size
        self.valid_trial_count

