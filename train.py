import json
import random
import string

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

# nltk.download("punkt") #! Just uncomment these from time to time to download the required packages
# nltk.download("wordnet")
# nltk.download("omw-1.4")

# initializing lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()
data = json.load(open('data.json',))

# Each list to create
words = []
classes = []
doc_X = []
doc_Y = []

# Loop through all the intents
# tokenize each pattern and append tokens to words, the patterns and
# the associated tag to their associated list

for intent in data["intents"]:
    for pattern in intent:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_Y.append(intent["tag"])
    
    # Add the tag to the classes list if it's not already there
    if intent["tag"] not in classes:
        classes.append(intent["tag"])

# lemmatize all the words in the vocab and convert them to lowercase
# if the words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]

# sorting the vocab and classes in alphabetical order and taking the 
# set of each to remove duplicates
words = sorted(set(words))
classes = sorted(set(classes))

# list for training data
training = []
out_empty = [0] * len(classes)
# creating the bag of words model
for idx, doc in enumerate(doc_X):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    
    # mark the index of the class that the current pattern is associated to
    output_row = list(out_empty)
    output_row[classes.index(doc_Y[idx])] = 1

    # add the one hot encoded Bow and associated classes to training
    training.append([bow, output_row])

# shuffle the data and convert it to an array
random.shuffle(training)
training = np.array(training, dtype=object)

# split the features and target labels
train_X = np.array(list(training[:, 0]))
train_Y = np.array(list(training[:, 1]))

# defining some parameters
input_shape = (len(train_X[0]),)
output_shape = len(train_Y[0])
epochs = 10 #! Change this to 2000 for better results

# the deep leaning model
model = Sequential()
model.add(Dense(128, input_shape=input_shape, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(output_shape, activation="softmax"))

adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)

model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])
print(model.summary())
model.fit(x=train_X, y=train_Y, epochs=epochs, batch_size=5, verbose=1)

def clean_text(text): 
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def bag_of_words(text, vocab): 
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens: 
        for idx, word in enumerate(vocab):
            if word == w: 
                bow[idx] = 1
    return np.array(bow)

def pred_class(text, vocab, labels): 
    bow = bag_of_words(text, vocab)
    print(bow)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list

def get_response(intents_list, intents_json): 
    tag = intents_list
    list_of_intents = intents_json["intents"]
    print(tag)
    for i in list_of_intents: 
        if i["tag"] == tag:
            result = i["responses"]
        break
    return result


# save the model
model.save("chatbot_model.h5", overwrite=True)

#load the model
model = tf.keras.models.load_model("chatbot_model.h5")


# running the chatbot
while True:
    message = input("You: ")
    intents = pred_class(message, words, classes)
    result = get_response(intents, data)
    print("Bot: ", result)
