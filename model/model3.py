import nltk
nltk.download('wordnet')
nltk.download('stopwords')

import spacy
from nltk.corpus import wordnet, stopwords
nlp = spacy.load("en_core_web_sm")

def process_text(text: str) -> dict:
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



a = process_text("If you want to customize multiple components of the language data or add support for a custom language or domain-specific “dialect”, you can also implement your own language subclass. I wish good luck to Maksim Krasotsky.")
for nc in a["noun_chunks"]:
   print(nc)
print("\n\n")
for ne in a["named_entities"]:
   print(ne)
print("\n\n")
for defs in a["all_def"]:
   print(defs)