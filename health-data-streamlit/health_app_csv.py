import streamlit as st
import pandas as pd
import os

st.title("🏥 Patienten-Logbuch (Lokal)")

csv_file = "patienten_daten.csv"

# Eingabe-Bereich
with st.form("input_form"):
    name = st.text_input("Patientenname")
    puls = st.number_input("Puls (bpm)", min_value=30, max_value=200, value=70)
    save_button = st.form_submit_button("In CSV speichern")

if save_button:
    # Neue Daten als DataFrame
    new_data = pd.DataFrame([[name, puls]], columns=["Name", "Puls"])
    
    # Prüfen, ob Datei existiert, und anhängen
    if not os.path.isfile(csv_file):
        new_data.to_csv(csv_file, index=False)
    else:
        new_data.to_csv(csv_file, mode='a', header=False, index=False)
    
    st.success(f"Daten für {name} lokal gesichert!")

# Anzeige der aktuellen CSV-Datei
st.divider()
st.subheader("Inhalt der lokalen CSV-Datei:")
if os.path.isfile(csv_file):
    df_display = pd.read_sql = pd.read_csv(csv_file)
    st.dataframe(df_display)
else:
    st.info("Die CSV-Datei existiert noch nicht.")