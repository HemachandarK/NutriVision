import streamlit as st
import pandas as pd

def predict():
    dataset_path = "DiseasePredict.csv"
    df = pd.read_csv(dataset_path)

    # Combine all symptom columns into a single list for each disease
    df['All_Symptoms'] = df[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 
                            'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 
                            'Symptom_9', 'Symptom_10', 'Symptom_11', 'Symptom_12', 
                            'Symptom_13', 'Symptom_14', 'Symptom_15', 'Symptom_16', 
                            'Symptom_17']].values.tolist()

    # Flatten symptom lists and remove NaN values
    df['All_Symptoms'] = df['All_Symptoms'].apply(lambda x: set(str(symptom).strip().lower() for symptom in x if pd.notna(symptom)))

    # Set the title of the Streamlit app
    st.title("Disease Prediction Based on Symptoms")

    # User input for symptoms
    user_input = st.text_input("Enter symptoms separated by commas (e.g., itching, skin_rash):")

    if user_input:
        # Split input symptoms into a list and clean up
        input_symptoms = set(symptom.strip().lower() for symptom in user_input.split(','))

        # Find matching diseases
        matched_diseases = df[df['All_Symptoms'].apply(lambda symptoms: bool(input_symptoms.intersection(symptoms)))]

        if not matched_diseases.empty:
            st.write("Based on the symptoms provided, the following diseases may be relevant:")
            for disease in matched_diseases['Disease'].unique():
                st.write(f"- {disease}")
        else:
            st.write("No matching diseases found for the symptoms provided.")
