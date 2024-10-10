import os
import sys

import spacy

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aigent.image_converter import ImageConverter

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a test sentence to verify that spaCy is working correctly.")

for token in doc:
    print(f"Token: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")