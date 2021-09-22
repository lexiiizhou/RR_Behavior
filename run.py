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
    bonsai_files = list_files(input_folder, '.')