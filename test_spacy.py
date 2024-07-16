import sys
print(sys.path)
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a test sentence to verify that spaCy is working correctly.")

for token in doc:
    print(f"Token: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")