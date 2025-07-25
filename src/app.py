# src/app.py

import streamlit as st
import joblib

# Load the trained model
model = joblib.load('model.pkl')  # Make sure the path is correct if the model is inside /models/

# Set up the Streamlit app UI
st.set_page_config(page_title="ML Predictor", layout="centered")
st.title("Spam Link Detector")

st.write("Enter a URL below to check if it's spam or not.")

# Input from the user
user_input = st.text_input("URL", "")

# Button to make prediction
if st.button("Predict"):
    if user_input:
        # Make prediction
        prediction = model.predict([user_input])[0]

        # Display result
        if prediction == 1:
            st.error("⚠️ This link is likely **SPAM**.")
        else:
            st.success("✅ This link is likely **SAFE**.")
    else:
        st.warning("Please enter a URL before clicking predict.")
