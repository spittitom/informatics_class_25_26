# Goal: Create a simple Streamlit application (streamlit_maiin.py) that visualizes 
# fictitious data on the reliability of various medical devices.

# Requirements
# 1. Title & Introduction: Give the app a relevant title and a brief description.
# 2. Data Preparation: Create a fictitious pandas DataFrame with the following columns:
#     Device_Type (e.g., CT, MRI, Ultrasound)
#     Maintenance_Cycles_pA (Number of maintenance events per year)
#     Reliability_Score (a fictitious value between 0 and 100)
#     Acquisition_Cost_in_K

# 3. Static Display: Display the complete DataFrame with a heading.

# 4. Interactive Visualization:
#     Add a Slider that allows the user to select a minimum Reliability Score.
#     Filter the DataFrame based on the slider's value.
#     Display the filtered data in a Bar Chart, visualizing the Device_Type (X-axis) and the corresponding Maintenance_Cycles_pA (Y-axis).

# pip install streamlit pandas
# streamlit run med_app.py


import streamlit as st
import pandas as pd


# application title
st.title("Medical Device Reliability Analysis Dashboard")
st.markdown("Analysis of fictitious maintenance data and reliability of various medical devices.")

# Data Preparation (Fictitious Dataset)
data = {
    'Device_Type': ['MRI', 'CT-Scanner', 'Ultrasound', 'ECG-Machine', 'Ventilator', 'Infusion_Pump'],
    'Maintenance_Cycles_pA': [5, 4, 2, 1, 3, 1],
    'Reliability_Score': [85, 92, 98, 99, 90, 95], # Fictitious Scores (0-100)
    'Acquisition_Cost_in_K': [2000, 1500, 100, 5, 50, 2]    
}
df = pd.DataFrame(data)

st.header("Raw Data Overview")
st.write("Overview of all recorded medical devices and their key metrics:")

# Display the DataFrame
st.dataframe(df)

# Interactive Visualization: Add Slider
st.header("Interactive Filtering by Reliability")
min_score = int(df['Reliability_Score'].min())
max_score = int(df['Reliability_Score'].max())
# The slider for the Reliability Score
reliability_filter = st.slider(
    'Select the minimum Reliability Score (0-100) for display:',
    min_value=min_score,
    max_value=max_score,
    value=90,  # Default value
    step=1
)
st.info(f"Only devices with a Reliability Score of **{reliability_filter}** or higher are shown.")

# Filtering the DataFrame
filtered_df = df[df['Reliability_Score'] >= reliability_filter]
st.subheader("Filtered Devices (Maintenance Cycles per Year)")
# Display the filtered DataFrame
st.dataframe(filtered_df)

# Displaying the filtered data in a Bar Chart
st.bar_chart(filtered_df.set_index('Device_Type')['Maintenance_Cycles_pA'])









# import streamlit as st
# import pandas as pd
# import numpy as np

# # 1. Application Title
# st.title("🏥 Medical Device Reliability Analysis Dashboard")
# st.markdown("Analysis of fictitious maintenance data and reliability of various medical devices.")

# # 2. Data Preparation (Fictitious Dataset)
# data = {
#     'Device_Type': ['MRI', 'CT-Scanner', 'Ultrasound', 'ECG-Machine', 'Ventilator', 'Infusion_Pump'],
#     'Maintenance_Cycles_pA': [5, 4, 2, 1, 3, 1],
#     'Reliability_Score': [85, 92, 98, 99, 90, 95], # Fictitious Scores (0-100)
#     'Acquisition_Cost_in_K': [2000, 1500, 100, 5, 50, 2]
# }
# df = pd.DataFrame(data)

# st.header("1. Raw Data Overview")
# st.write("Overview of all recorded medical devices and their key metrics:")
# # Display the DataFrame
# st.dataframe(df)

# # --- Interactive Section ---

# st.header("2. Interactive Filtering by Reliability")

# # 3. Interactive Visualization: Add Slider
# min_score = int(df['Reliability_Score'].min())
# max_score = int(df['Reliability_Score'].max())

# # The slider for the Reliability Score
# reliability_filter = st.slider(
#     'Select the minimum Reliability Score (0-100) for display:',
#     min_value=min_score,
#     max_value=max_score,
#     value=90,  # Default value
#     step=1
# )

# st.info(f"Only devices with a Reliability Score of **{reliability_filter}** or higher are shown.")

# # 4. Filtering the DataFrame
# filtered_df = df[df['Reliability_Score'] >= reliability_filter]

# st.subheader("Filtered Devices (Maintenance Cycles per Year)")
# # Display the filtered DataFrame
# st.dataframe(filtered_df)

# # 5. Displaying the filtered data in a Bar Chart
# # We use st.bar_chart() for a better visualization of individual device types
# st.bar_chart(filtered_df.set_index('Device_Type')['Maintenance_Cycles_pA'])