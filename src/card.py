# -*- coding: utf-8 -*-
import statistic


class Card:
    def __init__(self, en_word='', transcription='', ru_words=None):
        self.en_word = en_word
        self.transcription = transcription
        if ru_words == None:
            ru_words = []
        self.ru_words = map(lambda x: x.strip(), ru_words)
        self.statistic = {
            'en-ru': statistic.Statistic(),
            'ru-en': statistic.Statistic()
        }

    def pack(self):
        dic = {}
        for it in self.statistic:
            dic[it] = self.statistic[it].pack()
        return dic

    def unpack(self, stat):
        for it in stat:
            if it not in self.statistic:
                self.statistic[it] = statistic.Statistic()
            self.statistic[it].unpack(stat[it])

    def get_en_word(self):
        return self.en_word

    def get_quest(self, direction):
        if direction == 'en-ru':
            return self.en_word
        else:
            return u', '.join(self.ru_words)

    def get_transcription(self):
        return self.transcription

    def get_answer(self, direction):
        if direction == 'ru-en':
            return self.en_word
        else:
            return u', '.join(self.ru_words)

############################################################################
    def __str__(self):
        s = '' + self.en_word + ' ' + self.transcription + ' '
        for w in self.ru_words:
            s += (w + ', ')
        if s.endswith(', '):
            s = s[:-2]
        s += ' ' + str(self.statistic['en-ru'].percent)
        s += '/' + str(self.statistic['ru-en'].percent)
        return s.encode('utf-8')

if __name__ == '__main__':
    print Card(u'aback', u'əbˈæk', [u'захваченный врасплох', u'смущенный'])
