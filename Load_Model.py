import pickle
import numpy as np
import streamlit as st

WORD_DICT_PATH = 'models/word_dict.pkl'
CLASSIFIER_PATH = 'models/nb_classifier.pkl'

def load_artifacts():
    # Load saved artifacts
    with open(WORD_DICT_PATH, 'rb') as f:
        word_dict = pickle.load(f) 

    words = [w[0] for w in word_dict]  
        
    # Load classifier (adjust path if you saved to 'model/' instead)
    with open(CLASSIFIER_PATH, 'rb') as f:
        clf = pickle.load(f)
    return words, clf

def text_to_features(text, words):
    row_words = text.split()
    return np.array([row_words.count(w) for w in words]).reshape(1, -1)

# # Predict example
# X = text_to_features(email, words)
# pred = clf.predict(X)            # 1 = spam, 0 = ham (per your script)

# print("prediction:", "spam" if pred[0] == 1 else "ham")

st.title("Email Spam Classifier")
words, clf = load_artifacts()

placeholder_email = "Congratulations! You won a free ticket, click here"
text = st.text_area("Email text", placeholder=placeholder_email, height=150)

if st.button("Predict"):
    X = text_to_features(text, words)
    pred = clf.predict(X)[0]
    label = "spam" if pred == 1 else "ham"
    st.write("Prediction:", label)
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(X)[0]
        st.write("Probabilities:", {"ham": f"{probs[0]:.3f}", "spam": f"{probs[1]:.3f}"})