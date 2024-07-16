import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

import spacy
print(f"spaCy version: {spacy.__version__}")

import en_core_web_sm
print(f"en_core_web_sm version: {en_core_web_sm.__version__}")

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a test sentence.")
for token in doc:
    print(token.text, token.pos_)

print("SpaCy is working correctly!")