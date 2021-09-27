import pandas as pd
import list as ls
import re
from copy import deepcopy
import classes as cl

def preprocessing(filepath, eventcodedict):
    bonsai_output = pd.read_csv(filepath, names=['timestamp'])
    keys = list(eventcodedict.keys())

    bonsai_output['eventcode'] = bonsai_output['timestamp']. \
        map(lambda code: re.findall('[0-9]', code))
    bonsai_output['length'] = bonsai_output['eventcode'].map(lambda code: len(code))
    bonsai_output = bonsai_output[bonsai_output['length'] >= 13].drop(columns=['length'])

    bonsai_output['timestamp'] = bonsai_output['eventcode']. \
        map(lambda code: float("".join(code[:12])) / 1000)
    bonsai_output['eventcode'] = bonsai_output['eventcode']. \
        map(lambda code: int("".join(code[12:])))
    bonsai_output = bonsai_output[bonsai_output.eventcode.isin(keys)]. \
        reset_index(drop=True)

    bonsai_output['event'] = bonsai_output['eventcode']. \
        map(lambda code: eventcodedict[code])
    first_timestamp = bonsai_output.iloc[0, 0]
    firsthall = bonsai_output[bonsai_output['eventcode'] == 9].index[0]
    bonsai_output['timestamp'] = bonsai_output['timestamp']. \
        map(lambda t: (t - first_timestamp) / 1000)
    bonsai_output = bonsai_output[['event', 'timestamp', 'eventcode']]
    bonsai_output_final = bonsai_output[firsthall:]
    events_list = bonsai_output_final.values.tolist()

    def restaurant_extractor(events_list):
        for i in events_list:
            if len(i) <= 3:
                integers = re.findall('[0-9]+', i[0])
                for j in integers:
                    if 5 > int(j) > 0:
                        i.append(int(j))

    restaurant_extractor(events_list)

    return events_list


def detect_keyword_in_event(events):
    """
    events -- List: list of bonsai events
    """

    def detect_keyword(string):
        keyword = None
        if string.__contains__('hall'):
            keyword = 'hall'
        elif string.__contains__('zone'):
            keyword = 'offer zone'
        elif string.__contains__('offer'):
            probability = re.findall('[0-9]+', string)[1]
            keyword = probability + '_offer'
        elif string.__contains__('enter'):
            keyword = 'enter'
        elif string.__contains__('Quit'):
            keyword = 'quit'
        elif string.__contains__('no-reward'):
            keyword = 'noreward'
        elif string.__contains__('taken'):
            keyword = 'taken'
        elif string.__contains__('Servo'):
            keyword = 'servo'
        elif string.__contains__('Enter'):
            keyword = 'enter'
        elif string.__contains__('Reject'):
            keyword = 'reject'
        elif string.__contains__('Entry'):
            keyword = 'tentry'
        return keyword

    new_events_list = []
    for i in events:
        if len(i) < 5:
            i_description = i[0]
            i += [detect_keyword(i_description)]
            new_events_list.append(i)
        else:
            new_events_list.append(i)
    return new_events_list


def write_bonsaiEvent_dll(events_list):
    list_of_bonsaievents = ls.DoublyLinkedList()
    for i in events_list:
        event_object = cl.BonsaiEvent(i)
        list_of_bonsaievents.add_to_end(event_object)
    return list_of_bonsaievents


def write_dll_to_df(dll):
    df = pd.DataFrame.from_dict([dll.sentinel.next.info()])
    current = dll.sentinel.next.next
    while current != dll.sentinel:
        current_df = pd.DataFrame.from_dict([current.info()])
        df = pd.concat([df, current_df], axis=0)
        current = current.next
    df = df.drop(columns=['item', 'next','prev'])
    return df


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Represent Trials as a DLL of bonsai_event objects in the same restaurant"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_bonsai_event_item(item):
    """Create a new bonsai event object with next and prev = None"""
    new_object = cl.BonsaiEvent(item)
    return new_object


def trial_writer(events_list):
    current = events_list.sentinel.next
    i = 0
    trial = cl.Trial(get_bonsai_event_item(current.item), [current.item], i)
    current_restaurant = current.restaurant

    current = current.next
    trials = ls.DoublyLinkedList()

    while current != events_list.sentinel:
        if current.restaurant == current_restaurant:
            """mouse in the same restaurant"""
            trial.item.append(current.item)
        elif current.restaurant != current_restaurant:
            """mouse in a new restaurant"""
            trials.add_to_end(trial)
            trial = cl.Trial(get_bonsai_event_item(current.item), [current.item], i)
            trial.item.append(current.item)
            i += 1
        current_restaurant = current.restaurant
        current = current.next
    if i == 0:
        trials.add_to_end(trial)
    return trials


def getindex(lists, value):
    return next(i for i, v in enumerate(lists) if value in v)


def trial_info_filler(trials):
    """
    Fill in information about each trial by interating through all trials
    :param trials: DLL of Trial Objects
    :return: Modifies trials, returns nothing
    """
    current_trial = trials.sentinel.next
    while current_trial != trials.sentinel:  # current_trial is a Trial object
        """
        current_trial: Trial Object
        current_trial.sentinel.next.item: DLL of bonsai events
        current_trial.sentinel.next.item.sentinel.next: a single bonsai event with next and prev
        current_trial.sentinel.next.item.sentinel.next.restaurant: restaurant of that single bonsai event
        """

        """Fill Restaurant"""
        current_trial.restaurant = current_trial.item[0][-2]
        current_trial.enter = current_trial.item[0][1]
        current_trial.exit = current_trial.item[-1][1]

        """Detect Offer"""
        # Create a deep copy such that the original object variable won't be modified
        event_track = deepcopy(current_trial.item)

        """Write events"""
        for j in range(len(event_track)):
            if "_offer" in str(event_track[j]):
                sorted_list = [event_track[j]]
                current_trial.initiation = event_track[j][1]
                current_trial.tone_prob = event_track[j][-1].split('_')[0]
                if 'tentry' in str(event_track[j:]):
                    """check if tentry happened"""
                    tentry_index = getindex(event_track[j:], 'tentry')
                    current_trial.tEntry = event_track[tentry_index+j][1]
                    sorted_list.append(event_track[tentry_index + j])
                    if 'enter' in str(event_track[tentry_index:]):
                        """accepting offer"""
                        enter_index = getindex(event_track[tentry_index:], 'enter')
                        current_trial.choice = event_track[enter_index+tentry_index][1]
                        sorted_list.append(event_track[enter_index + tentry_index])
                        if 'servo' in str(event_track[enter_index:]):
                            servo_index = getindex(event_track[enter_index:], 'servo')
                            current_trial.reward = 1
                            current_trial.outcome = event_track[servo_index+enter_index][1]
                            sorted_list.append(event_track[servo_index+enter_index])
                            if 'taken' in str(event_track[servo_index:]):
                                taken_index = getindex(event_track[servo_index:], 'taken')
                                sorted_list.append(event_track[taken_index+servo_index])
                                current_trial.collection = event_track[taken_index+servo_index][1]
                                if 'quit' in str(event_track[taken_index]):
                                    """exit restaurant after obtaining reward"""
                                    quit_index = getindex(event_track[taken_index:], 'quit')
                                    sorted_list.append(event_track[quit_index+taken_index])
                                    current_trial.quit = 1
                                    current_trial.outcome = event_track[quit_index+taken_index][1]
                                    current_trial.termination = event_track[quit_index+taken_index][1]
                            elif 'quit' in str(event_track[servo_index:]):
                                """exit wait zone after servo open without taking pellets"""
                                quit_index = getindex(event_track[servo_index:], 'quit')
                                current_trial.quit = 1
                                current_trial.quit = event_track[quit_index+servo_index][1]
                                current_trial.termination = event_track[quit_index + servo_index][1]
                                sorted_list.append(event_track[quit_index+servo_index])
                        elif 'noreward' in str(event_track[enter_index:]):
                            noreward_index = getindex(event_track[enter_index:], 'noreward')
                            current_trial.outcome = event_track[noreward_index + enter_index][1]
                            current_trial.termination = event_track[noreward_index + enter_index][1]
                            sorted_list.append(event_track[noreward_index + enter_index])
                    elif 'reject' in str(event_track[tentry_index:]):
                        """existed t junction and went to the next restaurant"""
                        reject_index = getindex(event_track[tentry_index:], 'reject')
                        current_trial.termination = event_track[tentry_index + reject_index][1]
                        current_trial.choice = event_track[tentry_index + reject_index][1]
                        sorted_list.append(event_track[tentry_index + reject_index])
                elif 'reject' in str(event_track[j:]):
                    """rejecting offer and backtrack into the hallway in current restaurant"""
                    reject_index = getindex(event_track[j:], 'reject')
                    current_trial.choice = event_track[j+reject_index][1]
                    current_trial.termination = event_track[j+reject_index][1]
                    sorted_list.append(event_track[j+reject_index])

        # for i in range(len(event_track)):
        #     current_trial.enter = event_track[0][1]
        #     if "_offer" in str(event_track[i]):
        #         """
        #         offer tone played, trial initiated
        #         """
        #         current_trial.tone_prob = event_track[i][-1].split('_')[0]
        #         current_trial.initiation = event_track[i][1]
        #
        #         if 'reject' in str(event_track[i+1]):
        #             """
        #             Exiting offer zone and backtrack to current restaurant hallway
        #             """
        #             current_trial.choice = event_track[i+2][1]
        #             current_trial.termination = event_track[i+2][1]
        #         elif 'tentry' in str(event_track[i+1]):
        #             """enters t junction"""
        #             current_trial.tEntry = event_track[i+1][1]
        #             if 'reject' in str(event_track[i + 2]):
        #                 """
        #                 Exiting offer zone and enter next restaurant
        #                 """
        #                 current_trial.choice = event_track[i+2][1]
        #                 current_trial.termination = event_track[i+2][1]
        #             elif 'enter' in str(event_track[i + 2]):
        #                 """
        #                 if animal enters the restaurant: accept
        #                 """
        #                 current_trial.choice = event_track[i + 2][1]
        #
        #                 """Write outcome(reward, or noreward)"""
        #                 if "quit" in str(event_track[i+3]):
        #                     """Exiting restaurant"""
        #                     current_trial.outcome = event_track[i + 3][1]
        #                     current_trial.quit = 1
        #                     current_trial.termination = event_track[i + 3][1]
        #                 elif 'noreward' in str(event_track[i + 3]):
        #                     current_trial.outcome = event_track[i + 3][1]
        #                     current_trial.termination = event_track[i + 3][1]
        #                 elif 'servo' in str(event_track[i + 3]):
        #                     """
        #                     if servo arm opens, outcome presented
        #                     """
        #                     current_trial.reward = 1
        #                     current_trial.outcome = event_track[i + 3][1]
        #
        #                     """Write oucome collection"""
        #                     if 'taken' in str(event_track[i+4]):
        #                         current_trial.collection = event_track[i + 4][1]
        #                         current_trial.termination = event_track[i + 4][1]
        #                     elif "quit" in str(event_track[i+4]):
        #                         """
        #                         animal rejects pellet and move on to the next restaurant
        #                         """
        #                         current_trial.outcome = event_track[i+4][1]
        #                         current_trial.quit = 1
        #                         current_trial.termination = event_track[i+4][1]
        #     current_trial.exit = event_track[-1][1]
        current_trial = current_trial.next


def write_lap_block(trials):

    sequence = {
        1: 2,
        2: 3,
        3: 4,
        4: 1
    }

    current_trial = trials.sentinel.next
    if current_trial.initiation:
        current_trial.lapIndex, current_trial.blockIndex = 0, 0
    block = 0
    lap = 0
    current_trial = current_trial.next
    while current_trial != trials.sentinel:
        if current_trial.initiation:
            if current_trial.prev.initiation is None:
                block += 1
                lap = 0
            elif sequence[current_trial.prev.restaurant] == current_trial.restaurant:
                if current_trial.prev.restaurant == 4:
                    lap += 1
            current_trial.lapIndex = lap
            current_trial.blockIndex = block
        elif current_trial.initiation is None:
            if current_trial.prev.initiation:
                block += 1
            current_trial.blockIndex = block
        current_trial = current_trial.next


def write_trial_to_df(trials):
    """
    trials -- DLL: DLL representation of trials
    return -- dataFrame
    """
    current = trials.sentinel.next
    df = pd.DataFrame.from_dict([trials.sentinel.next.info()])
    while current != trials.sentinel:
        current_df = pd.DataFrame.from_dict([current.info()])
        df = pd.concat([df, current_df])
        current = current.next
    df = df.drop(columns=['item', 'firstEventNode', 'next', 'prev']).iloc[1:, :]
    df = df.rename(columns={'index': 'trial_index'}).set_index('trial_index')
    return df
