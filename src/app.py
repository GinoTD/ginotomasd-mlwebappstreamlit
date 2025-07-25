# src/app.py

import streamlit as st
import joblib
import os

# Load the model and vectorizer from the same folder
base_path = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_path, 'ridge_model.pkl'))
vectorizer = joblib.load(os.path.join(base_path, 'vectorizer.pkl'))

# Set up the Streamlit app UI
st.set_page_config(page_title="Spam Link Detector", layout="centered")
st.title("Spam Link Detector")

st.write("Enter a URL below to check if it's spam or not.")

# Input from the user
user_input = st.text_input("URL", "")

# Button to make prediction
if st.button("Predict"):
    if user_input:
        # Preprocess input using vectorizer
        X = vectorizer.transform([user_input.strip()])

        # Make prediction
        prediction = model.predict(X)[0]

        # Display result
        if prediction == 1:
            st.error("⚠️ This link is likely **SPAM**.")
        else:
            st.success("✅ This link is likely **SAFE**.")
    else:
        st.warning("Please enter a URL before clicking predict.")
