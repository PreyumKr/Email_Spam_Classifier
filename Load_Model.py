import pickle
import numpy as np
import streamlit as st
from transformers import pipeline

st.set_page_config(layout="wide")

WORD_DICT_PATH = 'models/word_dict.pkl'
CLASSIFIER_PATH = 'models/nb_classifier.pkl'

@st.cache_resource
def load_artifacts():
    # Load saved artifacts
    with open(WORD_DICT_PATH, 'rb') as f:
        word_dict = pickle.load(f) 

    words = [w[0] for w in word_dict]  
        
    # Load classifier (adjust path if you saved to 'model/' instead)
    with open(CLASSIFIER_PATH, 'rb') as f:
        clf = pickle.load(f)
    return words, clf

@st.cache_data
def text_to_features(text, words):
    row_words = text.split()
    return np.array([row_words.count(w) for w in words]).reshape(1, -1)

@st.cache_resource
def load_roberta():
    # Load the spam classification pipeline
    # spam_roberta = pipeline("text-classification", model="dima806/email-spam-detection-roberta")
    spam_roberta = pipeline("text-classification", model="roshana1s/spam-message-classifier")
    return spam_roberta


# # Predict example
# X = text_to_features(email, words)
# pred = clf.predict(X)            # 1 = spam, 0 = ham (per your script)

# print("prediction:", "spam" if pred[0] == 1 else "ham")

st.title("Email Spam Classifier")
words, clf = load_artifacts()
roberta_model = load_roberta()

placeholder_email = "Congratulations! You won a free ticket, click here"
st.markdown("### Enter Email Text")
text = st.text_area("Email text", placeholder=placeholder_email, height=150)

if st.button("Predict"):
    if not text.strip():
        st.warning("Please enter email text to classify.")
    else:
        col1, col2 = st.columns(2)
    
    X = text_to_features(text, words)
    pred = clf.predict(X)[0]
    label = "spam" if pred == 1 else "ham"
    col1.markdown("### Naive Bayes Prediction")
    col1.markdown(f"**Prediction:** {label}")
    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(X)[0]
        col1.markdown(f"**Probabilities:** Ham: {probs[0]:.3f}, Spam: {probs[1]:.3f}")

    roberta_result = roberta_model(text)[0]
    col2.markdown("### RoBERTa Prediction")
    col2.markdown(f"**Prediction:** {roberta_result['label']}")
    
    # Display probabilities based on the predicted label
    label = roberta_result['label'].lower()
    if label == 'ham':
        ham_score = roberta_result['score']
        spam_score = 1 - roberta_result['score']
    else:  # spam
        ham_score = 1 - roberta_result['score']
        spam_score = roberta_result['score']
    col2.markdown(f"**Probabilities:** Ham: {ham_score:.3f}, Spam: {spam_score:.3f}")