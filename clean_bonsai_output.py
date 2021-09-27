import copy


def clean_and_organize(events_list, lim=5):

    def clean_duplicates_and_events(events_list):
        """Delete duplicates and hall entries"""
        new_list = copy.deepcopy(events_list)
        for i in range(len(events_list)):
            if i < (len(events_list) - 2) and events_list[i][0] == events_list[i + 1][0]:
                new_list.remove(events_list[i + 1])
        return new_list


    events_list = clean_duplicates_and_events(events_list)

    def group_by_res(events_list):
        current_restaurant = events_list[0][-2]
        all_events = []
        event = [events_list[0]]
        for i in events_list[1:]:
            if i[-2] == current_restaurant:
                event.append(i)
            elif i[-2] != current_restaurant:
                all_events.append(event)
                event = [i]
                current_restaurant = i[-2]
        return all_events

    events_by_res = group_by_res(events_list)

    def clean_servos(events_list):
        """Delete servo open outputs that don't follow waitzone entry """
        new_list = copy.deepcopy(events_list)
        for i in range(len(events_list)):
            for j in range(len(events_list[i])):
                if len(events_list[i]) == 1 and events_list[i][0].__contains__('servo'):
                    """
                    if this sublist only contains a servo open, 
                    delete the entire sublist
                    """
                    new_list[i].remove(events_list[i][j])
                elif j == 0 and 'servo' in events_list[i][j]:
                    """
                    if servo is the first event in the sublist, 
                    """
                    new_list[i].remove(events_list[i][j])
                elif 1 < j <= (len(events_list[i]) - 1) and \
                        'servo' in events_list[i][j] and 'enter' not in events_list[i][j-1]:
                    new_list[i].remove(events_list[i][j])
        new_list = [x for x in new_list if x != []]
        return new_list

    events_by_res = clean_servos(events_by_res)


    i = 1
    while events_by_res[i] != events_by_res[-2]:
        if len(events_by_res[i]) <= 2:
            current_res = events_by_res[i][0][-2]
            front_index, front_steps = i - 1, 0
            while current_res != events_by_res[front_index][0][-2] and front_index >= 0:
                front_index -= 1
                front_steps += 1
                if front_steps >= lim or front_index < 0:
                    front_index = -1
                    front_steps = -1
            back_index, back_steps = i + 1, 0
            while current_res != events_by_res[back_index][0][-2] and back_index >= 0:
                back_index += 1
                back_steps += 1
                if back_steps >= lim or back_index >= (len(events_by_res) - 1):
                    back_index = -1
                    back_steps = -1

            new_ind = None
            if front_steps == -1 and back_steps != -1:
                new_ind = back_index
            elif back_steps == -1 and front_steps != -1:
                new_ind = front_index
            elif back_steps == -1 and front_steps == -1:
                events_by_res.pop(i)
            elif front_steps > back_steps:
                new_ind = back_index
            elif front_steps <= back_steps:
                new_ind = front_index

            if new_ind is not None and new_ind in range(len(events_by_res)):
                events_by_res[min(new_ind, i)] += events_by_res.pop(max(new_ind, i))
                i -= 2
        i += 1

    """
    If offer tone is the last event in a sublist, merge this sublist with the closest
    following that has the same restaurant number
     """
    # for i in range(len(events_by_res)):
    #     if "_offer" in events_by_res[i][-1][-1] and i <= (len(events_by_res) - 1):
    #         closest = i + 1
    #         while events_by_res[i][-1][-2] != events_by_res[closest][0][-2] and closest <= (len(events_by_res) - 1):
    #             closest += 1
    #         events_by_res[closest] = [events_by_res[i].pop(-1)] + events_by_res[closest]

    return sum(events_by_res, [])

