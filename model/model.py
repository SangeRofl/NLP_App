# -*- coding: utf-8 -*-
import nltk

nltk.download('wordnet')
nltk.download('stopwords')

import spacy
from nltk.corpus import wordnet, stopwords

import re
import pymorphy2

nlp = spacy.load("en_core_web_sm")


class Model:
    morph = pymorphy2.MorphAnalyzer()
    first_filter = True
    filter_mode = False
    
    TITLE_TYPES = ["noun_chunks", "named_entities", "all_def"]
    
    def __init__(self, view):
        self.view = view
        self.current_result = None
    
    def process_text(self, text: str) -> dict:
        doc = nlp(text)
        res = dict()
        res["noun_chunks"] = {}
        for chunk in doc.noun_chunks:
            res["noun_chunks"][str(chunk.text)] = [str(chunk.root), spacy.explain(chunk.root.dep_)]
        res["named_entities"] = {}
        for ent in doc.ents:
            res["named_entities"][str(ent.text)] = [spacy.explain(ent.label_)]
        res["all_def"] = {}
        for token in doc:
            if len(wordnet.synsets(token.text))!=0 and token.text not in stopwords.words():
                res["all_def"][token.text] = [wordnet.synsets(token.text)[0].definition()]
        return res

    def get_table_data(self):
        table = self.view.main_view.ui.tableWidget
        raw_data = {
            self.TITLE_TYPES[0]: {},
            self.TITLE_TYPES[1]: {},
            self.TITLE_TYPES[2]: {},
        }
        current_title = self.TITLE_TYPES[0]
        for row in range(table.rowCount()):
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if not item:
                    row_data.append('')
                elif (text := item.text()) in self.TITLE_TYPES:
                    current_title = text
                    break
                elif item.text():
                    row_data.append(item.text())  
                else:
                    row_data.append('')
            
            if row_data:
                raw_data[current_title][row_data[0]] = row_data[1:]
        
        print("result: ", raw_data)
        return raw_data
        
    def fill_table(self, res):
        self.current_result = res
        self.view.main_view.fill(res)
    
    def filter_table(self, text: str):
        if self.first_filter:
            self.refresh_current_result()
        self.first_filter = False
        self.filter_mode = True

        filter_result = {
            self.TITLE_TYPES[0]: {},
            self.TITLE_TYPES[1]: {},
            self.TITLE_TYPES[2]: {},
        }
        for i, word_set in enumerate(self.get_words()):
            for word in word_set:
                if word.startswith(text):
                    filter_result[self.TITLE_TYPES[i]][word] = self.current_result[self.TITLE_TYPES[i]][word]
        print("filter_result == current_result is ", filter_result == self.current_result)
        self.view.main_view.fill(filter_result)
        
    def get_words(self):
        words = []
        for i in self.current_result.values():
            words.append(list(i.keys()))
            
        return words
    
    def reset_table(self):
        if not self.filter_mode:
            self.refresh_current_result()
        self.first_filter = True
        self.filter_mode = False
        self.view.main_view.fill(self.current_result)
        
    def refresh_current_result(self):
        self.current_result = self.get_table_data()
