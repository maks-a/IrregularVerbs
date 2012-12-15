# -*- coding: utf-8 -*-
import dictionary
import datetime


class Lesson:
    def __init__(self, cfg_dict):
        self.cfg = cfg_dict
        self.dict = dictionary.Dictionary(cfg_dict)
        self.direction = 'ru-en'
        self.cards = self.dict.get_lesson_cards(self.direction)
        d = self.direction
        self.cards = sorted(self.cards, key=lambda c: c.statistic[d].percent)
        self.right_answer_counter = 0

    def set_new_card(self):
        self.current_card = self.cards.pop(0)

    def get_current(self):
        w = self.current_card
        d = self.direction
        return w.get_quest(d), w.transcription, w.get_answer(d), d

    def is_end(self):
        return (self.right_answer_counter >= self.cfg['cards_per_lesson']
            or len(self.cards) == 0)

    @staticmethod
    def convert_spec_chars(s):
        return s.replace(u'ё', u'е')

    def check_answer(self, answer, update_statistics):
        right_answer = self.current_card.get_answer(self.direction)
        is_right = False
        if self.direction == 'ru-en':
            is_right = answer.lower() == right_answer.lower()
        else:
            for w in right_answer.split(u', '):
                w = Lesson.convert_spec_chars(w)
                answer = Lesson.convert_spec_chars(answer)
                if answer.lower() == w.lower():
                    is_right = True
                    break
        if update_statistics:
            if is_right:
                self.right_answer()
            else:
                self.wrong_answer()
        return is_right

    def right_answer(self):
        self.right_answer_counter += 1
        self.change_statistic(abs(self.cfg['right_answer_percent']))

    def wrong_answer(self):
        self.change_statistic(-abs(self.cfg['wrong_answer_percent']))

    def change_statistic(self, delta):
        stat = self.current_card.statistic[self.direction]
        self.log('%d %+d %s' % (stat.percent, delta, self.direction))
        stat.percent = max(1, min(stat.percent + delta, 100))
        stat.history.append(int(delta > 0))
        history_len = 20
        stat.history = stat.history[-history_len:]
        self.current_card.statistic[self.direction] = stat

    def end_lesson(self):
        self.dict.save()
        self.dict.save_txt(self.direction)

    def log(self, message):
        with open('./data/log.txt', 'a+') as f:
            t = datetime.datetime.today().strftime("%Y.%m.%d %H:%M:%S")
            f.write('%s %s\n' % (t, message))
