import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

# 1. Verbindung zur Datenbank herstellen
# Wir holen uns die URL aus den Environment Variables (Sicherheit!)
DB_URL = os.environ.get("DATABASE_URL")

if DB_URL:
    engine = create_engine(DB_URL)
    
    st.title("🏥 Patienten-Datenbank (Persistent)")

    # Formular zum Speichern
    with st.form("patient_form"):
        name = st.text_input("Name")
        puls = st.number_input("Puls", min_value=30, max_value=250)
        submitted = st.form_submit_button("Speichern")

        if submitted:
            # Daten in die DB schreiben
            with engine.connect() as conn:
                conn.execute(
                    text("CREATE TABLE IF NOT EXISTS patients (name TEXT, puls INTEGER)")
                )
                conn.execute(
                    text("INSERT INTO patients (name, puls) VALUES (:n, :p)"),
                    {"n": name, "p": puls}
                )
                conn.commit()
            st.success(f"Daten für {name} wurden dauerhaft gespeichert!")

    # 2. Daten auslesen
    st.subheader("Gespeicherte Daten")
    try:
        df = pd.read_sql("SELECT * FROM patients", engine)
        st.dataframe(df)
    except:
        st.info("Noch keine Daten vorhanden.")
else:
    st.error("Datenbank-URL nicht gefunden! Bitte in Render unter Environment Variables eintragen.")