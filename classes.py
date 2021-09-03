import numpy
import pandas


class Event:
    """An event in a session"""

    def __init__(self, event, prev_event, next_event):
        self.prev_event = prev_event
        self.next_event = next_event
        self.restaurant
        self.offer  # True: offer tone ring | False: No Offer Tone Triggered
        self.duration
        """Keeping track of a log of events, regardless of event type"""


class Block:
    """A block of events defined by the direction of movement"""

    def __init__(self, block):
        self.counterclockwise = False


class Session:
    """Where trials and intermissions exist"""

    def __init__(self, events_list):
        """
        Create a session
        events_list -- List: a chronological list of events and timestamps [event, timestamp, event_code]
        """
        self.trial_count  # How many trials are in this session
        self.intermission_count  # How many intermissions are in this session
        self.events_list = events_list
        self.headEvent = None  # First event in the session

    def parse_event(self):

        pass

    def add_next_event(self, event, event_type):
        if event_type == 'Trial':
            newTrial = Trial()

        pass

    def event_count(self):
        return self.trial_count + self.intermission_count


class Trial(Block):
    """

    """

    type = 'Trial'

    def __init__(self, events):
        self.tone_prob
        self.restaurant
        self.choice  # True: Accept | False: reject
        self.re
        """Keep a log of only trials"""
        self.prev_trial
        self.next_trial

    def process_time_stamps(self):
        return

    def add_prev_trial(self):
        pass


class Intermission(Block):
    type = 'Intermission'

    def __init__(self, event_log):
        self.event_log = event_log

