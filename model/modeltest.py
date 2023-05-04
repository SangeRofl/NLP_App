import spacy
from nltk import WordNetLemmatizer

print(WordNetLemmatizer().lemmatize("greetings"))
nlp = spacy.load("ru_core_news_sm")
lemmatizer = nlp.get_pipe("lemmatizer")
print(lemmatizer.mode)  # 'rule'

doc = nlp("доброго человека.")
print(type(next(iter(doc)).lemma_))
# ['I', 'be', 'read', 'the', 'paper', '.'
