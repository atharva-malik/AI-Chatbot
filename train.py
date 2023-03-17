import json
import random
import string

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")
nltk.download("wordnet")

# initializing lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()
data = json.load(open('data.json',))

# Each list to create
words = []
classes = []
doc_X = []
doc_Y = []
print(data)
