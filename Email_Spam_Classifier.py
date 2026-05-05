import os
import pickle
import numpy as np
import pandas as pd
from logging import Logger
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


# Setup Logger



# Get the data from the csv file.
data = pd.read_csv("Dataset/combined_spam.csv")

data_clean = data.dropna()

words = []
for row in data_clean['text']:
    words +=  row.split(" ")

for i in range(len(words)):
    if not words[i].isalpha():
        words[i] = ""

word_dict = Counter(words)

del word_dict['']

word_dict = word_dict.most_common(3000)

feature_matrix = []
labels = []

for text, label in data_clean[['text', 'label']].values:
    data_count = []    
    row_words = text.split(" ")
    for word in word_dict:
        # print(word[0])
        data_count.append(row_words.count(word[0]))
    feature_matrix.append(data_count)

    if 'spam' in label:
        labels.append(1)
    if 'ham' in label:
        labels.append(0)

feature_matrix = np.array(feature_matrix)
labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(feature_matrix, labels, test_size=0.2, random_state=9)

classifier = MultinomialNB()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
accuracy_score(y_pred, y_test)

os.makedirs('models', exist_ok=True)

with open('models/word_dict.pkl', 'wb') as f:
    pickle.dump(word_dict, f, pickle.HIGHEST_PROTOCOL)

with open('models/nb_classifier.pkl', 'wb') as f:
    pickle.dump(classifier, f, protocol=pickle.HIGHEST_PROTOCOL)