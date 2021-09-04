import numpy
import pandas


class BonsaiEvent:
    def __init__(self, event):
        self.item = self
        self.event_description = event[0]
        self.timestamp = event[1]
        self.event_code = event[2]
        self.restaurant = event[3]
        self.keyword = event[4]
        self.prev = None
        self.next = None


class Trial:
    """
    Series of bonsai events in the same restaurant stored as
    a doubly linked list
    """

    def __init__(self, dll_of_bonsaievents, index):
        """
        events -- DLL: list of bonsai_event objects
        """
        self.valid = False  # True: Valid Trial
        self.tone_prob
        self.restaurant
        self.choice
        self.index
        self.current = self
        self.prev
        self.next


class Lap:
    """A doubly linked list of trials"""

    def __init__(self, dll_of_trials, direction, index):
        self.direction = direction
        self.index = index
        self.total_trial_count = dll_of_trials.size
        self.valid_trial_count
        self.current = self
        self.prev
        self.next


class Session:
    """A doubly linked list of laps"""

    def __init__(self, dll_of_laps):
        self.lap_count = dll_of_laps.size
        self.valid_trial_count

