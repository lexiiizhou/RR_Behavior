import pandas as pd
import copy
import list as ls
import re
import classes as cl


filePath = '/Users/lexizhou/Desktop/RR_bonsai_events_TS_reject.csv'


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
        elif string.__contains__('noreward'):
            keyword = 'noreward'
        elif string.__contains__('taken'):
            keyword = 'taken'
        elif string.__contains__('Servo'):
            keyword = 'servo'
        elif string.__contains__('Enter'):
            keyword = 'enter'
        elif string.__contains__('Reject'):
            keyword = 'reject'
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


events_list, event_code_dict = preprocessing(filePath)
events_list_with_keyword = detect_keyword_in_event(events_list)

"""Write events as bonsai_event objects"""


def clean_duplicates(events_list):
    new_list = copy.deepcopy(events_list)
    for j in range(len(events_list)):
        if j < len(events_list)-1 and events_list[j][0] == events_list[j+1][0]:
            new_list.remove(events_list[j])
    return new_list


def clean_rejections(events_list):
    new_list = copy.deepcopy(events_list)
    for j in range(len(events_list)):
        if j > 0 and events_list[j][-1] == 'reject':
            if "_offer" not in str(events_list[j-1][-1]):
                """rejection does not follow offer tone"""
                new_list.remove(events_list[j])
            elif events_list[j][-2] != events_list[j-1][-2]:
                new_list.remove(events_list[j])
    return new_list


def clean_quits(events_list):
    for j in range(len(events_list)):
        if j > 0 and events_list[j][-1] == 'quit':
            if "hall" in str(events_list[j-1][-1]):
                events_list[j-1], events_list[j] = events_list[j], events_list[j-1]
            elif events_list[j][-2] != events_list[j-1][-2]:
                index = j-1
                while events_list[index][-2] != events_list[j][-2]:
                    index -= 1
                events_list[index], events_list[j] = events_list[j], events_list[index]


events_list = clean_duplicates(events_list)
events_list = clean_rejections(events_list)
clean_quits(events_list)


list_of_bonsaievents = ls.DoublyLinkedList()
for i in events_list:
    event_object = cl.BonsaiEvent(i)
    list_of_bonsaievents.add_to_end(event_object)


def write_dll_to_df(dll):
    df = pd.DataFrame.from_dict([dll.sentinel.next.info()])
    current = dll.sentinel.next.next
    while current is not None:
        current_df = pd.DataFrame.from_dict([current.info()])
        df = pd.concat([df, current_df])
        current = current.next
    df = df.drop(columns=['item', 'current','next','prev'])
    return df


bonsaiEvent_df = write_dll_to_df(list_of_bonsaievents)
bonsaiEvent_df.to_csv('/Users/lexizhou/Desktop/bonsai.csv')


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Represent Trials as a DLL of bonsai_event objects in the same restaurant"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def get_bonsai_event_item(item):
    new_object = cl.BonsaiEvent(item)
    return new_object


def trial_writer(events_list):
    current = events_list.sentinel.next
    trial = ls.DoublyLinkedList()
    trial.add_to_end(get_bonsai_event_item(current.item))
    current_restaurant = current.restaurant

    current = current.next
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
            i += 1
        current_restaurant = current.restaurant
        current = current.next
    if i == 0:
        trials.add_to_end(cl.Trial(trial, i))
    return trials


def trial_info_filler(trials):
    """
    Fill in information about each trial by interating through all trials
    :param trials: DLL of Trial Objects
    :return: Modifies trials, returns nothing
    """
    current_trial = trials.sentinel.next
    while current_trial is not None:  # current_trial is a Trial object
        """
        current_trial: Trial Object
        current_trial.sentinel.next.item: DLL of bonsai events
        current_trial.sentinel.next.item.sentinel.next: a single bonsai event with next and prev
        current_trial.sentinel.next.item.sentinel.next.restaurant: restaurant of that single bonsai event
        """

        """Fill Restaurant"""
        current_trial.restaurant = current_trial.item.sentinel.next.restaurant

        """Detect Offer"""
        iterator = current_trial.item.sentinel.next
        event_track = []
        while iterator is not None:
            event_and_timestamp = []
            event_and_timestamp.append(iterator.keyword)
            event_and_timestamp.append(iterator.timestamp)
            event_track.append(event_and_timestamp)
            iterator = iterator.next

        def is_last(item, list):
            """check if item is the last of the list"""
            return item == list[-1]

        for i in range(len(event_track)):
            current_trial.enter = event_track[0][1]
            if "_offer" in str(event_track[i]):
                current_trial.tone_prob = event_track[i][0].split('_')[0]
                current_trial.initiation = event_track[i][1]

                """Write choice"""
                if is_last(event_track[i], event_track):
                    """
                    if offer tone is the last event in this trial, terminate
                    trial_type = reject
                    """
                    current_trial.choice = event_track[i][1]
                    current_trial.termination = event_track[i][1]
                elif 'reject' in str(event_track[i + 1]):
                    """
                    Exiting offer zone
                    """
                    current_trial.choice = event_track[i+1][1]
                    current_trial.termination = event_track[i][1]
                elif 'enter' in str(event_track[i + 1]):
                    """
                    if animal enters the restaurant: accept
                    """
                    current_trial.choice = event_track[i + 1][1]

                    """Write outcome(reward, or noreward)"""
                    if "quit" in str(event_track[i+2]):
                        """Exiting restaurant"""
                        current_trial.outcome = event_track[i + 2][1]
                        current_trial.quit = True
                        current_trial.termination = event_track[i + 2][1]
                    elif 'noreward' in str(event_track[i + 2]):
                        current_trial.outcome = event_track[i + 2][1]
                        current_trial.reward = False
                        current_trial.termination = event_track[i + 2][1]
                    elif 'servo' in str(event_track[i + 2]):
                        """
                        if servo arm opens, outcome presented
                        """
                        current_trial.reward = True
                        current_trial.outcome = event_track[i + 2][1]

                        """Write oucome collection"""
                        if 'taken' in str(event_track[i+3]):
                            current_trial.collection = event_track[i + 3][1]
                            current_trial.termination = event_track[i + 3][1]
                        elif "quit" in str(event_track[i+3]):
                            """
                            animal rejects pellet and move on to the next restaurant
                            """
                            current_trial.outcome = event_track[i+3][1]
                            current_trial.quit = True
                            current_trial.termination = event_track[i+3][1]
            current_trial.exit = event_track[-1][1]
        current_trial = current_trial.next


trials = trial_writer(list_of_bonsaievents)
trial_info_filler(trials)


def write_trial_to_df(trials):
    """
    trials -- DLL: DLL representation of trials
    return -- dataFrame
    """
    current = trials.sentinel.next
    df = pd.DataFrame.from_dict([trials.sentinel.next.info()])
    while current is not None:
        current_df = pd.DataFrame.from_dict([current.info()])
        df = pd.concat([df, current_df])
        current = current.next
    df = df.drop(columns=['item', 'current', 'next', 'prev']).iloc[1:, :]
    df = df.rename(columns={'index': 'trial_index'}).set_index('trial_index')
    return df


trials_df = write_trial_to_df(trials)
trials_df.to_csv('/Users/lexizhou/Desktop/trials.csv')
