import streamlit as st
import pandas as pd

def foodsuggest():
    dataset_path = "modified_dataset.csv"
    df = pd.read_csv(dataset_path)

    # Set the title of the Streamlit app
    st.title("Food and Disease Finder")

    # User input for the food name
    food_name = st.text_input("Enter the name of the food:")

    # Check if user input is provided
    if food_name:
        # Filter the dataset based on the food name
        filtered_df = df[df['Name'].str.contains(food_name, case=False, na=False)]
        
        if not filtered_df.empty:
            st.write(f"The food '{food_name}' may be beneficial when the following diseases are present:")
            disease_set = set()
            for _, row in filtered_df.iterrows():
                diseases = row['Disease']
                disease_set.add(diseases)

            # Print the unique diseases at the end
            st.write("Diseases:")
            for disease in disease_set:
                st.write(disease)
        else:
            st.write(f"No diseases found for the food item '{food_name}'.")
