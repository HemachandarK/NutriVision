import streamlit as st
import pandas as pd

# Load the dataset
dataset_path = "DiseasePrecaution.csv"  # Change this to the path of your CSV file
df = pd.read_csv(dataset_path)

# Set the title of the Streamlit app
st.title("Disease Precaution Finder")

# User input for disease name
disease_name = st.text_input("Enter the name of the disease:")

if disease_name:
    # Look for the disease name in the dataset
    matched_precautions = df[df['Disease'].str.lower() == disease_name.lower()]
    
    if not matched_precautions.empty:
        st.write(f"Precautions for {disease_name}:")
        for index, row in matched_precautions.iterrows():
            precautions = [
                row['Precaution_1'],
                row['Precaution_2'],
                row['Precaution_3'],
                row['Precaution_4']
            ]
            for i, precaution in enumerate(precautions, start=1):
                if pd.notna(precaution) and precaution.strip():
                    st.write(f"- Precaution {i}: {precaution}")
    else:
        st.write(f"No precautions found for the disease '{disease_name}'.")
