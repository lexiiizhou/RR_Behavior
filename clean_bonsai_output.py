import copy


def clean_and_organize(events_list, lim=5):

    def clean_duplicates(events_list):
        """Delete duplicates and hall entries"""
        new_list = copy.deepcopy(events_list)
        for i in range(len(events_list)):
            if i < (len(events_list) - 1) and events_list[i][0] == events_list[i + 1][0]:
                new_list.remove(events_list[i + 1])
        return new_list

    events_list = clean_duplicates(events_list)

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

    return sum(events_by_res, [])

