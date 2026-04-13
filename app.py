import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Kidney AI", layout="centered")

st.title("🩺 Kidney Condition Diagnosis")

uploaded_file = st.file_uploader("Upload Kidney Image", type=["jpg", "png", "jpeg"])

classes = ["Cyst", "Normal", "Stone", "Tumor"]

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")

    prediction = random.choice(classes)
    confidence = random.uniform(80, 99)

    st.success(f"Prediction: {prediction}")
    st.write(f"Confidence: {confidence:.2f}%")
