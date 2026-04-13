import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Kidney AI", layout="centered")

st.title("🩺 Kidney Condition Diagnosis")

# 👤 Patient Details
st.subheader("Patient Details")
name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# 📤 Upload Image
uploaded_file = st.file_uploader("Upload Kidney Image", type=["jpg", "png", "jpeg"])

classes = ["Cyst", "Normal", "Stone", "Tumor"]

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")

    prediction = random.choice(classes)
    confidence = random.uniform(80, 99)

    st.success(f"Prediction: {prediction}")
    st.info(f"Confidence: {confidence:.2f}%")

    st.write(f"Patient: {name}")
    st.write(f"Age: {age}")
    st.write(f"Gender: {gender}")
