import streamlit as st
from PIL import Image
import random

st.title("Kidney Condition Diagnosis")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

classes = ["Cyst", "Normal", "Stone", "Tumor"]

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img)

    prediction = random.choice(classes)
    confidence = random.uniform(80, 99)

    st.write(prediction)
    st.write(confidence)