import streamlit as st
import pandas as pd

# Load the dataset
data_path = "modified_dataset.csv"  # Replace with the correct path if different
df = pd.read_csv(data_path)

# Function to get food suggestions based on disease and region
def get_food_suggestions(disease, region):
    # Filter data based on disease and region
    filtered_df = df[df['Disease'].str.contains(disease, case=False, na=False)]
    filtered_df = filtered_df[filtered_df['Region'].str.contains(region, case=False, na=False)]
    return filtered_df.head(10)  # Return only the top 10 records

# Streamlit app
st.title("Food and Nutrition Suggestions")
st.header("Get food suggestions and nutritional information based on disease and region")

# User input for disease name
disease_name = st.text_input("Enter a disease name:")

# User input for region
region_name = st.text_input("Enter a region:")

# Add a search button
if st.button("Search"):
    # Display suggestions if both disease name and region are provided
    if disease_name and region_name:
        suggestions = get_food_suggestions(disease_name, region_name)
        if not suggestions.empty:
            st.write(f"Here are the top 10 food suggestions for {disease_name} in {region_name}:")
            st.dataframe(suggestions)
        else:
            st.write("No food suggestions found for the given disease and region.")
    else:
        st.write("Please enter both a disease name and a region to get food suggestions.")
