import pandas as pd
import numpy as np
import list as ls
import re
import classes as cl


filePath = '/Users/lexizhou/Desktop/RR_bonsai_events_TS.csv'


def preprocessing(filepath):
    events = pd.read_csv(filepath)
    events = events.rename(columns={'9':"event_code", events.columns[0]: 'event', '246.7670912': 'timestamp'})
    if len(events.columns) > 3:
        events = events.drop(events.columns[3], axis=1)
    if 'Unnamed: 3' in events.columns:
        events = events.drop(columns=['Unnamed: 3'])
    events['event'] = events['event'].str.replace('[^\w\s]', '')

    event_code_dic = events.groupby(['event', 'event_code']).size()
    event_code_dic = event_code_dic.to_frame().reset_index().set_index('event_code')
    event_code_dict = event_code_dic.to_dict()['event']

    events_list = events.values.tolist()

    def restaurant_extractor(events_list):
        for i in events_list:
            if len(i) <= 3:
                integers = re.findall('[0-9]+', i[0])
                for j in integers:
                    if 5 > int(j) > 0:
                        i.append(int(j))

    restaurant_extractor(events_list)
    return events_list, event_code_dict


def detect_keyword_in_event(events_list):
    """
    event -- List: list of bonsai events
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
        elif string.__contains__('noreward'):
            keyword = 'noreward'
        elif string.__contains__('taken'):
            keyword = 'taken'
        elif string.__contains__('servo'):
            keyword = 'servo'
        elif string.__contains__('Enter'):
            keyword = 'enter'
        elif string.__contains__('Reject'):
            keyword = 'reject'
        return keyword

    new_events_list = []
    for i in events_list:
        if len(i) < 5:
            i_description = i[0]
            i += [detect_keyword(i_description)]
            new_events_list.append(i)
        else:
            new_events_list.append(i)
    return new_events_list


events_list, event_code_dict = preprocessing(filePath)
events_list_with_keyword = detect_keyword_in_event(events_list)

"""Write events as bonsai_event objects"""
list_of_bonsaievents = ls.DoublyLinkedList()
for i in events_list[:30]:
    event_object = cl.BonsaiEvent(i)
    list_of_bonsaievents.add_to_end(event_object)


"""Represent Trials as a DLL of bonsai_event objects in the same restaurant"""


def get_bonsai_event_item(item):
    new_object = cl.BonsaiEvent(item)
    return new_object


def trial_writer(events_list):
    current_restaurant = events_list.sentinel.next.restaurant
    current = events_list.sentinel.next.next
    trial = ls.DoublyLinkedList()
    trial.add_to_end(get_bonsai_event_item(events_list.sentinel.next.item))
    trials = ls.DoublyLinkedList()
    i = 0
    while current is not None:
        if current.restaurant == current_restaurant:
            """mouse in the same restaurant"""
            bonsai_event = get_bonsai_event_item(current.item)
            trial.add_to_end(bonsai_event)
        elif current.restaurant != current_restaurant:
            """mouse in a new restaurant"""
            trials.add_to_end(cl.Trial(trial, i))
            trial = ls.DoublyLinkedList()
            trial.add_to_end(get_bonsai_event_item(current.item))
            i+=1
        current_restaurant = current.restaurant
        current = current.next
    if i == 0:
        trials.add_to_end(cl.Trial(trial, i))
    return trials


def trial_info_filler(trials):
    """
    Fill in informations about each trial
    :param trials: DLL of Trial Objects
    :return: Modifies trials, returns nothing
    """
    current_trial = trials.head
    while current_trial is not None:  # current_trial is a Trial object
        """
        current_trial: Trial Object
        current_trial.head.item: DLL of bonsai events
        current_trial.head.item.head: a single bonsai event with next and prev
        current_trial.head.item.head.restaurant: restaurant of that single bonsai event
        """

        """Fill Restaurant"""
        current_trial.restaurant = current_trial.item.head.restaurant

        """Detect if it is a valid trial"""
        iterator = current_trial.item.head
        event_track = []
        while iterator is not None:
            event_track.append(iterator.keyword)
            iterator = iterator.next
        if len(event_track) >= 3:
            """should contain at least hall->offerZone->Reject"""


        current_trial = current_trial.next

