# 1. Purpose: The Streamlit application is a prototype for managing clinical trials, 
# enabling patient registration, study data validation, and analysis of the collected 
# information in a single web app.
# 2. Registration & Validation: The Registration tab uses internal forms and a 
# simulated API check (NCT-ID) to validate patient data and temporarily store it 
# in $st.session\_state$.
# 3. Analysis & API Testing: Two additional tabs display the stored patient data in a 
# DataFrame and a chart for analysis, while a separate API Explorer tab performs a real 
# live query of the ClinicalTrials.gov API to verify trial details.

import streamlit as st
import pandas as pd
import requests

CLINICAL_TRIAL_API_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
st.sidebar.caption(f"Used API Endpoint (Base): {CLINICAL_TRIAL_API_BASE_URL}")

if 'patients' not in st.session_state:
    st.session_state['patients'] = []
    
def fetch_real_study_details(nct_id):
    if not nct_id:
        return None
    
    url = f"{CLINICAL_TRIAL_API_BASE_URL}/{nct_id}"
    with st.spinner(f'Querying real ClinicalTrials.gov API for {nct_id}...'):
        try:
            response = requests.get(url, timeout=5) 
            response.raise_for_status() 
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching from API ({url}): {e}")
            return None 

def submit_patient_with_api_check():
    nct_id = st.session_state.nct_id.upper().strip()
    age = st.session_state.age
    bp = st.session_state.blood_pressure
    arm = st.session_state.study_arm
    
    new_patient = {
        'NCT_ID': nct_id,
        'Age': age,
        'Blood_Pressure': bp,
        'Study_Arm': arm,
        'Registration_Date': pd.Timestamp.now().strftime("%Y-%m-%d")
    }
    
    st.session_state.patients.append(new_patient)
    st.success(f"Patient successfully registered! Linked to study ID: **{nct_id}**")    


st.title("Clinical Trial Registration with API Validation")
st.markdown("Demonstrating $st.session\_state$, $st.form$, and external API integration.")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["➕ Patient Registration", "📊 Study Analysis", "🌐 API Explorer (Live)"])

with tab1:
    st.header("Patient Enrollment & API Check (Simulated)")
    
    with st.form("patient_api_form"):
        st.subheader("Enter Study and Patient Data")
        
        st.text_input("NCT ID of the Study (e.g., NCT12345678):", key='nct_id', value="NCT12345678")
        st.divider()
        st.number_input("Age (Years):", min_value=18, max_value=99, value=30, step=1, key='age')
        st.number_input("Systolic Blood Pressure (mmHg):", min_value=50, max_value=250, value=120, step=1, key='blood_pressure')
        st.selectbox("Assigned Study Arm:", options=['Placebo', 'Drug A', 'Drug B'], key='study_arm')
        
        st.form_submit_button("Save Patient & Check NCT ID (API)", on_click=submit_patient_with_api_check)
    
with tab2:
    st.header("Current Study Data")
    
with tab3: 
    st.header("🌐 Live ClinicalTrials.gov API Lookup")
    st.info("This tab executes a REAL API call using the 'requests' library.")
    
    DEFAULT_NCT = "NCT06572735"
    
    input_nct = st.text_input(
        "Enter an NCT Number:",
        value=DEFAULT_NCT
    )
    
    if st.button("Fetch Study Details"):
        if not input_nct.upper().startswith("NCT"):
             st.warning("Please enter a valid NCT number (starting with NCT).")
             
        api_data = fetch_real_study_details(input_nct.upper())
        
        try:
            title = api_data['protocolSection']['identificationModule']['officialTitle']
            status = api_data['protocolSection']['statusModule']['overallStatus']
            st.success(f"**Title:** {title}")
            st.write(f"**Current Status:** {status}")
        except (KeyError, IndexError):
            st.warning("Structure not found or no study found for this ID.")
            
        st.markdown("---")
        st.subheader("Full JSON Response (Debugging)") 
        st.json(api_data)















# import streamlit as st
# import pandas as pd
# import time
# import requests 

# # --- Global API Constant (Updated ClinicalTrials.gov API v2 URL) ---
# CLINICAL_TRIAL_API_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
# st.sidebar.caption(f"Used API Endpoint (Base): {CLINICAL_TRIAL_API_BASE_URL}")

# # --- 1. Session State Initialization ---
# if 'patients' not in st.session_state:
#     st.session_state['patients'] = []

# # --- 2. API Function for Study Validation (Simulated for Registration Stability) ---
# def check_study_via_api_simulated(nct_id):
#     """
#     Simulates the call to the ClinicalTrials.gov API (v2) for NCT ID validation.
#     Used for the stable registration process.
#     """
    
#     # Simulate invalid IDs and error cases for demo purposes
#     if nct_id.upper() in ["NCT00000000", "TEST-FAIL"]:
#         st.error(f"❌ API Error: Study ID {nct_id} not found in external database (Simulated).")
#         return None, None, False
    
#     with st.spinner(f'Checking NCT ID "{nct_id}" with ClinicalTrials.gov API (Simulated)...'):
#         time.sleep(1.5)
        
#         # Simulate successful API response
#         study_title = f"Interventional Study {nct_id} for Long-term Effects"
#         study_status = "Recruiting" if not nct_id.endswith('1') else "Completed"
            
#         return study_title, study_status, True

# # --- 3. Callback Function for the Form (with API Logic) ---
# def submit_patient_with_api_check():
#     """Validates input, checks the study via simulated API, and saves data."""
    
#     # Retrieve data from Session State
#     nct_id = st.session_state.nct_id.upper().strip()
#     age = st.session_state.age
#     bp = st.session_state.blood_pressure
#     arm = st.session_state.study_arm
    
#     # Local Validation
#     if not nct_id or not (18 <= age <= 90):
#         st.error("Please enter a valid NCT ID (e.g., NCT12345678) and ensure age is between 18 and 90.")
#         return

#     # API Validation (Using the SIMULATED function)
#     study_title, study_status, api_success = check_study_via_api_simulated(nct_id)
    
#     if not api_success:
#         return

#     # Save patient data if validation is successful
#     new_patient = {
#         'NCT_ID': nct_id,
#         'Study_Title': study_title,
#         'Study_Status': study_status,
#         'Age': age,
#         'Blood_Pressure': bp,
#         'Study_Arm': arm,
#         'Registration_Date': pd.Timestamp.now().strftime("%Y-%m-%d")
#     }
    
#     st.session_state.patients.append(new_patient)
#     st.success(f"✅ Patient successfully registered! Linked to study: **{study_title}** (Status: {study_status})")


# # --- 4. NEW FUNCTION: Real API Call ---
# def fetch_real_study_details(nct_id):
#     """Executes a real API call to ClinicalTrials.gov."""
#     if not nct_id:
#         return None
        
#     url = f"{CLINICAL_TRIAL_API_BASE_URL}/{nct_id}"
    
#     with st.spinner(f'Querying real ClinicalTrials.gov API for {nct_id}...'):
#         try:
#             response = requests.get(url, timeout=5) 
#             response.raise_for_status() 
#             data = response.json()
#             return data
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ Error fetching from API ({url}): {e}")
#             return None


# # --- 5. Streamlit Application with THREE Tabs ---

# st.title("🔬 Clinical Trial Registration with API Validation")
# st.markdown("Demonstrating $st.session\_state$, $st.form$, and external API integration.")

# # Create the tabs
# tab1, tab2, tab3 = st.tabs(["➕ Patient Registration", "📊 Study Analysis", "🌐 API Explorer (Live)"])

# # === TAB 1: Patient Registration ===
# with tab1:
#     st.header("Patient Enrollment & API Check (Simulated)")
    
#     with st.form("patient_api_form"):
#         st.subheader("Enter Study and Patient Data")
        
#         st.text_input("NCT ID of the Study (e.g., NCT12345678):", key='nct_id', value="NCT12345678")
#         st.divider()
#         st.number_input("Age (Years):", min_value=18, max_value=99, value=30, step=1, key='age')
#         st.number_input("Systolic Blood Pressure (mmHg):", min_value=50, max_value=250, value=120, step=1, key='blood_pressure')
#         st.selectbox("Assigned Study Arm:", options=['Placebo', 'Drug A', 'Drug B'], key='study_arm')
        
#         st.form_submit_button("Save Patient & Check NCT ID (API)", on_click=submit_patient_with_api_check)


# # === TAB 2: Study Analysis ===
# with tab2:
#     st.header("Current Study Data")
    
#     if not st.session_state.patients:
#         st.info("No patient data has been registered yet.")
#     else:
#         df_patients = pd.DataFrame(st.session_state.patients)
        
#         st.subheader(f"Total Registered Patients: {len(df_patients)}")
        
#         st.markdown("### 1. Raw Data")
#         st.dataframe(df_patients) 
        
#         st.markdown("### 2. Distribution by Study Arm")
        
#         arm_counts = df_patients['Study_Arm'].value_counts().reset_index()
#         arm_counts.columns = ['Study_Arm', 'Count']
        
#         st.bar_chart(arm_counts.set_index('Study_Arm'))


# # === TAB 3: API Explorer (Live) ===
# with tab3:
#     st.header("🌐 Live ClinicalTrials.gov API Lookup")
#     st.info("This tab executes a REAL API call using the 'requests' library.")
    
#     DEFAULT_NCT = "NCT06572735"
    
#     input_nct = st.text_input(
#         "Enter an NCT Number:", 
#         value=DEFAULT_NCT
#     )
    
#     if st.button("Fetch Study Details"):
#         if not input_nct.upper().startswith("NCT"):
#              st.warning("Please enter a valid NCT number (starting with NCT).")
#         else:
#             api_data = fetch_real_study_details(input_nct.upper())
            
#             if api_data:
#                 st.subheader(f"Results for NCT ID: {input_nct.upper()}")
                
#                 try:
#                     # Accessing nested JSON structure
#                     study = api_data#['studies'][0]
#                     title = study['protocolSection']['identificationModule']['officialTitle']
#                     status = study['protocolSection']['statusModule']['overallStatus']
                    
#                     st.success(f"✅ **Title:** {title}")
#                     st.write(f"**Current Status:** {status}")
                    
#                 except (KeyError, IndexError):
#                     st.warning("Structure not found or no study found for this ID.")
                
#                 st.markdown("---")
#                 st.subheader("Full JSON Response (Debugging)")
#                 st.json(api_data)