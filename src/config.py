# -*- coding: utf-8 -*-
import json_com

default_config = {
    'path_to_dict': 'dict.json',
    'path_to_stat': 'statistic.json',
    'sounds_folder': './sounds',
    'cards_per_lesson': 10,
    'study_cards_num': 50,
    'right_answer_percent': 10,
    'wrong_answer_percent': 50,
    'retry_time_sec': 1200,
    'hide_transcription': 'no'
}


class Config():
    def __init__(self, path):
        self.path = path

    def get_dic(self):
        dic = json_com.parse(self.path)
        for key in default_config.keys():
            dic[key] = dic.get(key, default_config[key])
        return dic
