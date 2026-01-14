import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="HealthMonitor", page_icon="❤️", layout="wide")
st.title("Patient Health Data Monitor")

csv_file = "patient_data.csv"

with st.form("input_form"):
    name = st.text_input("Name of the Patient")
    age = st.slider("Age", 1, 100, 25)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (m)", min_value=0.50, max_value=2.50, value=1.70)
    save_button = st.form_submit_button("Save Data in CSV")

if save_button:
    new_data = pd.DataFrame([[name, age, weight, height]], columns=["Name", "Age", "Weight", "Height"])
    
    bmi = weight / (height ** 2)
    st.subheader(f"Patient: {name}, Age: {age}")
    st.write(f"Weight: {weight} kg")
    st.write(f"Height: {height} m")
    st.write(f"Body Mass Index (BMI): {bmi:.2f}")
    
    if bmi < 18.5:
        st.warning("Underweight")
    elif 18.5 <= bmi < 24.9:
        st.success("Normal weight")
    elif 25 <= bmi < 29.9:
        st.warning("Overweight")
    else:
        st.error("Obesity")
    
    if not os.path.isfile(csv_file):
        new_data.to_csv(csv_file, index=False)
    else:
        new_data.to_csv(csv_file, mode='a', header=False, index=False)
        
    st.success(f"Data for {name} saved successfully!")
    
st.divider()
st.subheader("Content of the local CSV-file:")
if os.path.isfile(csv_file):
    df_display = pd.read_csv(csv_file)
    st.dataframe(df_display)
else:
    st.info("No data available. Please add patient data above.")
