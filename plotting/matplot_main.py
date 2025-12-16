# Create a Python function that accepts a list of patient or subject data (Age, Weight, Height), calculates 
# the Body Mass Index (BMI) for each, and visualizes the distribution of BMI in relation to age using a 
# combined Matplotlib figure.

# Requirements
# a) Data Structure: The input data should be a list of tuples (e.g., [(Age, Weight_kg, Height_m), ...]).
# b) BMI Calculation: Implement a function to calculate the BMI: $BMI = \frac{Weight\ (kg)}{Height\ (m)^2}$.
# c) Visualization with Matplotlib (Subplots):
# 	- Create a single figure containing two subplots (1 row, 2 columns).
# 	- Subplot 1 (Scatter Plot): Plot Age (x-axis) against BMI (y-axis). Include horizontal lines to 
#     represent standard BMI classifications (Underweight, Normal Weight, Overweight, Obesity).
# 	- Subplot 2 (Histogram): Plot the frequency distribution of the calculated BMI values. Include 
#     vertical lines to represent the standard BMI classification thresholds.
# 	- Label all axes, provide clear titles for both plots, and include a legend.

# pip install matplotlib

import matplotlib.pyplot as plt
#import numpy as np

# --- 1. Helper function for BMI calculation ---
def calculate_all_bmi(patient_data: list) -> list:
    """Calculates the BMI for all patients in the list. (Weight/Height^2)"""
    weight = [p[1] for p in patient_data]
    height = [p[2] for p in patient_data]
    
    # Error handling for invalid data
    if any(h <= 0 for h in height):
        raise ValueError("Height must be positive.")
        
    return [w / (h ** 2) for w, h in zip(weight, height)]

# --- 2. Main function with Subplots ---
def visualize_bmi_analysis(patient_data: list):
    """
    Creates a combined Matplotlib figure (Scatter Plot and Histogram) 
    for analyzing patient BMI distribution.
    
    :param patient_data: A list of tuples: 
                         [(Age, Weight_kg, Height_m), ...]
    """
    
    try:
        age = [p[0] for p in patient_data]
        bmi_values = calculate_all_bmi(patient_data)
    except ValueError as e:
        print(f"Error during data processing: {e}")
        return

    # BMI Classification Thresholds (WHO)
    underweight_max = 18.5
    normal_weight_max = 24.9
    overweight_max = 29.9
    
    # Create figure (fig) and two axes (axes) side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    plt.suptitle('Comprehensive Body Mass Index (BMI) Analysis', fontsize=16)
    
    # ------------------------------------------------------------------
    # --- Subplot 1: Scatter Plot (BMI vs. Age) ---
    # ------------------------------------------------------------------
    ax1 = axes[0]
    
    # Scatter Plot
    ax1.scatter(age, bmi_values, color='darkblue', label='Patient BMI', alpha=0.7)
    
    # Horizontal Classification Lines
    ax1.axhline(y=underweight_max, color='orange', linestyle=':', linewidth=1.5, label='Underweight (18.5)')
    ax1.axhline(y=normal_weight_max, color='green', linestyle='-', linewidth=1.5, label='Normal Weight (24.9)')
    ax1.axhline(y=overweight_max, color='red', linestyle='--', linewidth=1.5, label='Overweight (29.9)')
    
    # Labels
    ax1.set_title('BMI vs. Age (Scatter Plot)')
    ax1.set_xlabel('Age (Years)')
    ax1.set_ylabel('Body Mass Index (BMI)')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_ylim(15, 40) 

    # ------------------------------------------------------------------
    # --- Subplot 2: Histogram (BMI Distribution) ---
    # ------------------------------------------------------------------
    ax2 = axes[1]
    
    # Histogram
    ax2.hist(bmi_values, bins=8, color='skyblue', edgecolor='black', alpha=0.7, 
             label='BMI Frequency')
    
    # Vertical Classification Lines
    ax2.axvline(x=underweight_max, color='orange', linestyle=':', 
                linewidth=2, label='Underweight Threshold (18.5)')
    ax2.axvline(x=normal_weight_max, color='green', linestyle='-', 
                linewidth=2, label='Normal Weight Threshold (24.9)')
    ax2.axvline(x=overweight_max, color='red', linestyle='--', 
                linewidth=2, label='Overweight Threshold (29.9)')
                
    # Labels
    ax2.set_title('Frequency Distribution of BMI (Histogram)')
    ax2.set_xlabel('Body Mass Index (BMI)')
    ax2.set_ylabel('Number of Patients (Frequency)')
    
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Adjust X-limit for better visualization of lines
    min_bmi = min(bmi_values) * 0.95
    max_bmi = max(bmi_values) * 1.05
    ax2.set_xlim(min(15, min_bmi), max(40, max_bmi))
    
    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Uncomment the line below to show the plot when running the script
    plt.show()


# --- 3. Sample Data ---
# Format: (Age (Years), Weight (kg), Height (m))
sample_patient_data = [
    (25, 75, 1.80), (55, 95, 1.75), (30, 50, 1.65), 
    (42, 88, 1.90), (60, 70, 1.70), (19, 110, 1.85),
    (75, 65, 1.60), (33, 60, 1.75), (48, 80, 1.78), 
    (22, 55, 1.55), (35, 105, 1.80), (50, 68, 1.70),
    (65, 92, 1.65), (38, 72, 1.85), (28, 62, 1.68)
]

# --- 4. Execution of the combined visualization ---
visualize_bmi_analysis(sample_patient_data)