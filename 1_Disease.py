import streamlit as st
import pandas as pd

# Load the dataset
data_path = "dataset.csv"
df = pd.read_csv(data_path)

# Function to get food suggestions based on disease
def get_food_suggestions(disease):
    suggestions = df[df['Disease'].str.contains(disease, case=False, na=False)]
    return suggestions

# Streamlit app
st.title("Food and Nutrition Suggestions")
st.header("Get food suggestions and nutritional information based on disease")

# User input for disease name
disease_name = st.text_input("Enter a disease name:")

# Display suggestions if a disease name is provided
if disease_name:
    suggestions = get_food_suggestions(disease_name)
    if not suggestions.empty:
        st.write("Here are some food suggestions for", disease_name, ":")
        st.dataframe(suggestions)
    else:
        st.write("No food suggestions found for the given disease name.")
else:
    st.write("Please enter a disease name to get food suggestions.")
