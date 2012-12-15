# -*- coding: utf-8 -*-
import card
import json
import json_com
import random
import os.path


class Dictionary:
    def __init__(self, cfg_dic):
        self.cfg = cfg_dic
        self.reload()
        self.check_sounds()
        self.save()

    def reload(self):
        raw_dic = json_com.parse(self.cfg['path_to_dict'])
        stat = json_com.parse(self.cfg['path_to_stat'])
        self.cards = set()
        for en_word, transcription, ru_words in raw_dic:
            c = card.Card(en_word, transcription, ru_words.split(','))
            if en_word in stat:
                c.unpack(stat[en_word])
            self.cards.add(c)

    def get_done_percent(self, direction):
        done = 0
        for c in self.cards:
            if c.statistic[direction].percent >= 100:
                done += 1
        return int(done * 100 / len(self.cards))

    def save(self):
        stat_json = {}
        for c in self.cards:
            percent = (c.statistic['en-ru'].percent +
                       c.statistic['ru-en'].percent)
            if percent > 0:
                stat_json[c.get_en_word()] = c.pack()
        json.dump(stat_json, open(self.cfg['path_to_stat'], 'wb'), indent=2)

    def save_txt(self, direction):
        stat_txt = {}
        for c in self.cards:
            stat_txt[c.get_en_word()] = c.statistic[direction].percent
        path = self.cfg['path_to_stat']
        path = path.replace('.json', '.txt')
        with open(path, 'wb') as f:
            for k in sorted(stat_txt, key=lambda k: stat_txt[k], reverse=True):
                line = '{:>3}\t{}'.format(str(stat_txt[k]), k)
                f.write(line + '\n')

    def get_lesson_cards(self, direction):
        def comp(c):
            stat = c.statistic
            rating = stat[direction].percent
            random.seed()
            if 0 < rating < 100:
                return (1, random.randrange(1, 10))
            elif rating == 0:
                return (2, random.randrange(1, 10))
            else:
                return (3, random.randrange(1, 10))
        dic = sorted(self.cards, key=comp)
        study_cards_num = self.cfg['study_cards_num']
        return dic[:study_cards_num]

    def check_sounds(self):
        sounds_dir = self.cfg['sounds_folder']
        missing = []
        for c in self.cards:
            filename = c.en_word + '.wav'
            if not os.path.isfile(os.path.join(sounds_dir, filename)):
                missing.append(filename)

        output_file = os.path.join(sounds_dir, 'check_sounds_report.txt')
        with open(output_file, 'w') as f:
            f.write('Missing files:\n')
            for filename in sorted(missing):
                f.write('"' + filename + '"\n')
