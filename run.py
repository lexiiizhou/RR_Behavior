from mainAnalysis import *
import os


def list_files(dir, type):
    """
    List all files of a certain type in the given dir
    :param dir: directory
    :param type: str
    :return:
    """
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(type):
                r.append(os.path.join(root, name))
    return r


def write_trials(input_folder):
    """
    take in bonsai log files and output trial csv
    :param input_folder: folder that contains bonsai log files, doesn't need to be homogenous
    :return:
    """
    bonsai_files = list_files(input_folder, '.csv')
    for file in bonsai_files:
        pathPrefix = os.path.dirname(file)
        sessionname = str(file).split('/')[-1].split('.')[0]
        events, event_code_dict = preprocessing(filePath)
        events_list = clean.clean_and_organize(detect_keyword_in_event(events))
        list_of_bonsaievents = write_bonsaiEvent_dll(events_list)

        bonsaiEvent_df = write_dll_to_df(list_of_bonsaievents)
        bonsaiEvent_df.to_csv(pathPrefix + sessionname + ".csv")

        trials = trial_writer(list_of_bonsaievents)
        trial_info_filler(trials)
        write_lap_block(trials)

        trials_df = write_trial_to_df(trials)
        trials_df.to_csv(pathPrefix + sessionname + "_trials.csv")
