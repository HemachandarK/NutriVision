import streamlit as st
import pandas as pd

# Load the datasets
description_dataset_path = "DiseaseDescription.csv"  # Replace with the correct path if different
precaution_dataset_path = "DiseasePrecaution.csv"    # Replace with the correct path if different

description_df = pd.read_csv(description_dataset_path)
precaution_df = pd.read_csv(precaution_dataset_path)

# Set the title of the Streamlit app
st.title("Disease Information Finder")

# User input for disease name
disease_name = st.text_input("Enter the name of the disease:")

# Adding a search button
if st.button("Search"):
    if disease_name:
        # Look for the disease name in the description dataset
        matched_description = description_df[description_df['Disease'].str.lower() == disease_name.lower()]['Description']
        
        # Look for the disease name in the precaution dataset
        matched_precautions = precaution_df[precaution_df['Disease'].str.lower() == disease_name.lower()]
        
        if not matched_description.empty:
            st.write(f"**Description of {disease_name}:**")
            st.write(matched_description.iloc[0])
        else:
            st.write(f"No description found for the disease '{disease_name}'.")
        
        if not matched_precautions.empty:
            st.write(f"**Precautions for {disease_name}:**")
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
    else:
        st.write("Please enter a disease name to search.")

