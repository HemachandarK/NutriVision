import streamlit as st
from streamlitimage import findimage
from food_log import main_1
from Home import home
from DiseaseDescription import description
from Disease import disease
from DiseasePredict import predict
from FoodSuggest import foodsuggest

def main():
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Dietmanagement", "Findimage","Disease","DiseaseDescription","DiseasePredict","FoodSuggest"])

    if page == "Home":
        home()
    elif page == "Findimage":
        findimage()
    elif page == "Dietmanagement":
        main_1()
    elif page == "DiseaseDescription":
        description()
    
    elif page == "DiseasePrediction":
        predict()
    elif page == "Disease":
        disease()
    elif page == "FoodSuggest":
        foodsuggest()
    

if __name__ == "__main__":
    main()
