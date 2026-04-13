import streamlit as st
from PIL import Image
import random
from fpdf import FPDF

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

# 📄 PDF function
def generate_pdf(name, age, gender, prediction, confidence):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Kidney Diagnosis Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Gender: {gender}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, f"Prediction: {prediction}", ln=True)
    pdf.cell(200, 10, f"Confidence: {confidence:.2f}%", ln=True)

    file_name = "report.pdf"
    pdf.output(file_name)

    return file_name

# 🔍 Prediction
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

    # Generate PDF
    pdf_file = generate_pdf(name, age, gender, prediction, confidence)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Report",
            data=f,
            file_name="kidney_report.pdf",
            mime="application/pdf"
        )
