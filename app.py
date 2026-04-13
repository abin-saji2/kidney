import streamlit as st
from PIL import Image
import requests
from fpdf import FPDF
import sqlite3
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Kidney AI", layout="centered")

st.title("🩺 Kidney Condition Diagnosis")

# 👤 Patient Details
st.subheader("Patient Details")
name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# 📤 Upload Image
uploaded_file = st.file_uploader("Upload Kidney Image", type=["jpg", "png", "jpeg"])

# 🗄️ Database setup
conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    condition TEXT,
    confidence REAL,
    date TEXT
)
""")

conn.commit()

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

# 🔍 Prediction using API
if uploaded_file is not None:

    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")

    # 🔥 CALL API (LOCAL)
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        files={"file": uploaded_file.getvalue()}
    )

    result = response.json()

    prediction = result["prediction"]
    confidence = result["confidence"]

    st.success(f"Prediction: {prediction}")
    st.info(f"Confidence: {confidence:.2f}%")

    st.write(f"Patient: {name}")
    st.write(f"Age: {age}")
    st.write(f"Gender: {gender}")

    # 💾 Save to DB
    cursor.execute(
        "INSERT INTO history (name, age, gender, condition, confidence, date) VALUES (?, ?, ?, ?, ?, ?)",
        (
            name,
            age,
            gender,
            prediction,
            confidence,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    conn.commit()

    # 📄 Generate PDF
    pdf_file = generate_pdf(name, age, gender, prediction, confidence)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Report",
            data=f,
            file_name="kidney_report.pdf",
            mime="application/pdf"
        )

# 📊 Show History
st.subheader("📊 Prediction History")

df = pd.read_sql_query("SELECT * FROM history", conn)
st.dataframe(df)
