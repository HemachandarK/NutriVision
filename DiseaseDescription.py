import streamlit as st
import pandas as pd

# Load the dataset
dataset_path = "DiseaseDescription.csv"  # Replace with the correct path if different
df = pd.read_csv(dataset_path)

# Set the title of the Streamlit app
st.title("Disease Description Finder")

# User input for disease name
disease_name = st.text_input("Enter the name of the disease:")

if disease_name:
    # Look for the disease name in the dataset
    matched_description = df[df['Disease'].str.lower() == disease_name.lower()]['Description']
    
    if not matched_description.empty:
        st.write(f"Description of {disease_name}:")
        st.write(matched_description.iloc[0])
    else:
        st.write(f"No description found for the disease '{disease_name}'.")
