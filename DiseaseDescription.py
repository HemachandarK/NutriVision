import streamlit as st
import pandas as pd

def description():
    dataset_path = "DiseaseDescription.csv" 
    precaution_dataset_path = "DiseasePrecaution.csv"    # Replace with the correct path if different

    df = pd.read_csv(dataset_path)
    precaution_df = pd.read_csv(precaution_dataset_path)# Replace with the correct path if different


    # Set the title of the Streamlit app
    st.title("Disease Description And Information Finder")

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
        

        matched_description = df[df['Disease'].str.lower() == disease_name.lower()]['Description']
            
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
    
