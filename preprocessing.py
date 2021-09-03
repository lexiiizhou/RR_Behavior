import pandas as pd

"""Plug Things In Here"""
file_path = ...

events = pd.read_csv(file_path)
events = events.rename(columns={'9':"event_code", 'Mouse in hall 1': 'event', '246.7670912': 'timestamp'})
events = events.drop(columns=['0'])
events['event'] = events['event'].str.replace('[^\w\s]','')

"""Make a dictionary that stores event code and their corresponding event"""
event_code_dic = events.groupby(['event', 'event_code']).size()
event_code_dic = event_code_dic.to_frame().reset_index().set_index('event_code')
event_code_dict = event_code_dic.to_dict()['event']

"""Convert dataFrame to a list of timestamps"""
events_list = events.values.tolist()


