import streamlit as st
import mysql.connector
import food_log
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
    act = st.selectbox('Activity Level', ['sedentary', 'lightly active', 'moderately active','very active','extra active'])
    if st.button('Submit'):
        if name and email and password and age > 0:
            # Database connection
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',  
                    password='hemsmysql3',
                    database='food_det'  
                )
                cursor = conn.cursor()
                query = """
                INSERT INTO food_det (name, email, password, gender, age, height, weight,act_lvl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, password, gender, age, height, weight,act))
                conn.commit()
                
                st.success('User details submitted successfully! Please Refresh the Page')
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            st.error('Please fill all the required fields')
    
        

