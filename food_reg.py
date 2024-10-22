import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import pytz
ist = pytz.timezone('Asia/Kolkata')
ist_time = datetime.now(ist)
# Connect to MongoDB
client=MongoClient('mongodb+srv://hemachandark333:hems@cluster0.45yyp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['food_det_db']  # Database
users_collection = db['user_details']  # Collection for storing user details

def reg():
    st.title('Food Recognition and Nutrition Analysis')
    st.header('User Details')
    
    name = st.text_input('Name', max_chars=30) 
    email = st.text_input('Email') 
    password = st.text_input('Password', max_chars=30, type='password') 
    gender = st.selectbox('Gender', ['Male', 'Female', 'Others'])
    age = st.number_input('Age', min_value=0, max_value=120, step=1) 
    height = st.number_input('Height (cm)', min_value=0.0, max_value=300.0, step=0.1, format='%f')
    weight = st.number_input('Weight (kg)', min_value=0.0, max_value=500.0, step=0.1, format='%f')
    act = st.selectbox('Activity Level', ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'])
    
    if st.button('Submit'):
        if name and email and password and age > 0:
            # Insert user details into MongoDB
            try:
                user_data = {
                    'name': name,
                    'email': email,
                    'password': password,
                    'gender': gender,
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'activity_level': act,
                    'last_update':ist_time
                }
                
                users_collection.insert_one(user_data)  # Insert into MongoDB
                st.success('User details submitted successfully! Please Refresh the Page')
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error('Please fill all the required fields')
