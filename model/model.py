# -*- coding: utf-8 -*-
import nltk
import re
import pymorphy2

from nltk.tokenize import word_tokenize, sent_tokenize


nltk.download('punkt')


class Model:
    morph = pymorphy2.MorphAnalyzer()
    first_filter = True
    filter_mode = False
    
    def __init__(self, view):
        self.view = view
        self.current_result = None
    
    def process_text(self, text: str) -> dict:
        res = dict()
        sentences = sent_tokenize(text.lower())
        words = []
        
        for j in [word_tokenize(i) for i in sentences]:
            words += j
        
        for i in words:
            lemma = Model.morph.parse(i)[0].normal_form
            if not re.match('^[а-яА-ЯёЁ]+$', lemma):
                continue 

            if lemma not in res.keys():
                res[lemma] = dict()
                res[lemma][i] = [1, '']
            else:
                if i not in res[lemma].keys():
                    res[lemma][i] = [1, '']
                else:
                    res[lemma][i][0] += 1
        
        
        self.fill_table(res)
        return res           
    
    def get_table_data(self):
        table = self.view.main_view.ui.tableWidget
        raw_data = []
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    value = [item.text(), item.font().bold()] if column == 0 else item.text()
                    row_data.append(value)  
                else:
                    row_data.append(['', False]) if column == 0 else row_data.append('')
                
            raw_data.append(row_data)
        
        # process raw_data
        result = {'': {}}
        prev_key = None
        for item in raw_data:
            key, value1, value2 = item
            try:
                if key[1]:
                    result[key[0]] = {}
                    prev_key = key[0]
                elif prev_key:
                    result[prev_key][key[0]] = [value1, value2]
                else:
                    result[''][key[0]] = [value1, value2]
            except IndexError:
                pass

        print("result: ", result)
        return result
        
    def fill_table(self, res):
        self.current_result = res
        self.view.main_view.fill(res)
    
    def filter_table(self, text: str):
        if self.first_filter:
            self.refresh_current_result()
        self.first_filter = False
        self.filter_mode = True

        filter_result = self.current_result.copy()
        for lexem in self.current_result.keys():
            if not lexem.startswith(text):
                del filter_result[lexem]

        self.view.main_view.fill(filter_result)
        
    def reset_table(self):
        if not self.filter_mode:
            self.refresh_current_result()
        self.first_filter = True
        self.filter_mode = False
        self.view.main_view.fill(self.current_result)
        
    def refresh_current_result(self):
        self.current_result = self.get_table_data()
