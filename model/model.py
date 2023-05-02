# -*- coding: utf-8 -*-
import nltk
import re
import pymorphy2
import spacy

from nltk.tokenize import word_tokenize, sent_tokenize


nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")


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
    
    def process_sentence(self, sentence: str) -> list:
        res = {}
        doc = nlp(sentence)
        for token in doc:
            token_text = token.text
            if not re.match(r"\b[A-Za-z]+\b", token_text):
                continue

            token_pos = spacy.explain(str(token.pos_))
            token_dep = spacy.explain(str(token.dep_))
            # token_pos = token.pos_
            # token_dep = token.dep_
            token_head = token.head.text
            res[token_text] = [token_pos, token_dep, token_head]
        return res         
    
    def get_table_data(self):
        table = self.view.main_view.ui.tableWidget
        raw_data = []
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    row_data.append(item.text())  
                else:
                    row_data.append('')
    
            raw_data.append(row_data)
        
        # process raw_data
        result = {}
        for item in raw_data:
            key, values = item[0], item[1:]
            result[key] = values
    
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
        for word in self.current_result.keys():
            if not word.startswith(text):
                del filter_result[word]

        self.view.main_view.fill(filter_result)
        
    def reset_table(self):
        if not self.filter_mode:
            self.refresh_current_result()
        self.first_filter = True
        self.filter_mode = False
        self.view.main_view.fill(self.current_result)
        
    def refresh_current_result(self):
        self.current_result = self.get_table_data()
