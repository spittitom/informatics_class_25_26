import streamlit as st

st.set_page_config(page_title="Health Monitor", page_icon="🏥")

st.title("🏥 Patient Health Check")

with st.sidebar:
    st.header("Patienten-Daten")
    name = st.text_input("Name des Patienten")
    age = st.slider("Alter", 1, 100, 25)

col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Gewicht (kg)", min_value=1.0, value=70.0)
with col2:
    height = st.number_input("Größe (m)", min_value=0.5, value=1.75)

if st.button("Analyse starten"):
    bmi = weight / (height ** 2)
    st.subheader(f"Ergebnis für {name}:")
    st.metric(label="BMI", value=f"{bmi:.2f}")
    
    if bmi < 18.5:
        st.warning("Untergewicht")
    elif 18.5 <= bmi < 25:
        st.success("Normalgewicht")
    else:
        st.error("Übergewicht")
    
    st.info(f"Patientenalter: {age} Jahre")