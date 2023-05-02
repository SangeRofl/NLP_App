import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

def process_sentence(sentence: str) -> list:
    res = []
    doc = nlp(sentence)
    for token in doc:
        token_text = token.text
        token_pos = spacy.explain(str(token.pos_))
        token_dep = spacy.explain(str(token.dep_))
        # token_pos = token.pos_
        # token_dep = token.dep_
        token_head = token.head.text
        res.append([token_text, token_pos, token_dep, token_head])
    return res

for i in process_sentence("Some english text"):
    print(i)