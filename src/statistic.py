# -*- coding: utf-8 -*-


class Statistic:
    def __init__(self):
        self.percent = 0
        self.history = []

    def pack(self):
        data = {}
        data['percent'] = self.percent
        data['history'] = self.history
        return data

    def unpack(self, data):
        self.percent = data['percent']
        self.history = data['history']
