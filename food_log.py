import streamlit as st
from pymongo import MongoClient
import food_reg
from bson import ObjectId
from streamlitimage import findimage

import pandas as pd
from fuzzywuzzy import process
from decimal import Decimal
from online_order import online_order
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
ist = pytz.timezone('Asia/Kolkata')
ist_time = datetime.now(ist)
client = MongoClient("mongodb://localhost:27017/")
db = client['food_det_db']  # Database name
users_collection = db['user_details']  # Collection name
goals_collection = db['goals'] 

def verify_user(email, password):
    try:
        # Query to find user with the given email and password
        user = users_collection.find_one({"email": email, "password": password})
        
        if user:
            # If user is found, return their name and id
            return user['name'], str(user['_id'])
        else:
            # If no user is found, return None
            return None
    except Exception as err:
        st.error(f"Error: {err}")
        return None

def verify_user_goal(user_id):
    try:
        # Query the MongoDB collection
        result = goals_collection.find_one({"user_id": user_id})
        
        if result:
            return result.get('goal', None)  # Return the goal if it exists
        else:
            return None  # User not found

    except Exception as err:
        st.error(f"Error: {err}")
        return None

def log():
  

   
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('New User? Go to Registration'):
        st.session_state.current_page = 'reg'
        st.rerun()
    if st.button('Login'):
        if email and password:
            user = verify_user(email, password)
            if user:
                st.success('Login successful!')
                st.session_state.current_page = 'h_main'
                st.session_state.current_user=user
                st.rerun()
            else:
                st.error('Invalid email or password. Please try again.')
        else:
            st.error('Please enter both email and password.')


def search_food(food_name, df):
    food_name = food_name.lower()
    choices = df['Name'].tolist()
    match, score = process.extractOne(food_name, choices)
    if score >= 80:  # Adjust score threshold as needed
        food_details = df[df['Name'] == match]
        return food_details
    else:
        return pd.DataFrame()


def food_item(fp):
    data = pd.read_csv(fp)
    st.title('Food Nutrient Lookup')
    food_choices = data['Name'].unique().tolist()
    
    # This will hold the selected food name
    food_item = st.selectbox('Enter the name of the food item:', options=food_choices)
    
    if st.button('Submit'):
        if food_item:
            results = search_food(food_item, data)
            if not results.empty:
                # Display the DataFrame without index using st.dataframe()
                st.dataframe(results.style.hide(axis='index'))
            else:
                st.write('Food item not found. Please check the spelling or try another item.')
        else:
            st.write('Please enter a food item.')
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button('Back'):
            st.session_state.current_page = 'h_main'
            st.rerun()
    with col2:
        if st.button('Logout'):
            st.session_state.current_page = 'log'
            st.rerun()
            
def h_main():
    st.header(f"Hi {st.session_state.current_user[0]}!")

    # Place other buttons in the main column
    col1, col2, col3 ,col4 = st.columns(4)  # Creates 3 equally spaced columns
    
    with col1:
        if st.button('Nutritional Analysis'):
            st.session_state.current_page = 'food_item'
            st.rerun()
    
    with col2:
        if st.button('Diet Management'):
            st.session_state.current_page = 'diet'
            st.rerun()
    
    with col3:
        if st.button('Update Profile'):
            st.session_state.current_page = 'up_prof'
            st.rerun()
    with col4:
        if st.button('Check My Orders'):
            st.session_state.current_page = 'online_order'
            st.rerun()
    if st.button('Logout'):
        st.session_state.current_page = 'log'
        st.rerun()



        
def goal_reg(user_id, goal):
    try:
        # Upsert operation: Insert a new document if it does not exist, otherwise update the existing one
        result = goals_collection.update_one(
            
            {"user_id": ObjectId(user_id)},  # Query to find the document
            {"$set": {"goal": goal, "user_id": user_id}},  # Update operation
            upsert=True  # Create a new document if no matching document is found
        )

        if result.matched_count > 0:
            st.success('Goal updated successfully!')
        else:
            st.success('Goal set successfully!')

    except Exception as err:
        st.error(f"Error: {err}")

def goal_update(user_id, goal):
   
    try:
        # Upsert operation: Insert a new document if it does not exist, otherwise update the existing one
        result = goals_collection.update_one(
            {"user_id": user_id},  # Query to find the document
            {"$set": {"goal": goal, "user_id": user_id}},  # Update operation
            upsert=True  # Create a new document if no matching document is found
        )

        if result.matched_count > 0:
            st.success('Goal updated successfully!')
        else:
            st.success('Goal set successfully!')

    except Exception as err:
        st.error(f"Error: {err}")

def food_search(f,d):
    f_list=[]
    for i in f:
        food_name = i.lower()
        choices = d['Name'].tolist()
        match, score = process.extractOne(food_name, choices)
        if score >= 70:  
            food_details = d[d['Name'] == match]
            # Select only the necessary columns
            required_columns = ['Protein [g]', 'Fat [g]', 'Carbohydrate [g]', 'Energy [KJ]']
            f_list.append(food_details[required_columns])
    return f_list

def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


def cal_daily(height, weight, age, sex, activity_level, category):
    height = to_float(height)
    weight = to_float(weight)
    age = to_float(age)
    
    # Harris-Benedict equation for BMR calculation
    if sex == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    # Activity factor based on activity level
    activity_factors = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }
    
    # Calculate TDEE
    tdee = bmr * activity_factors[activity_level]
    
    # Adjust daily caloric goal based on category
    if category == 'Maintain Weight':
        daily_caloric_goal = tdee
    elif category == 'Gain Weight':
        daily_caloric_goal = tdee + 500
    elif category == 'Lose Weight':
        daily_caloric_goal = tdee - 500
    else:
        daily_caloric_goal = tdee  # Default to maintain if unknown category
    return int(daily_caloric_goal)


def calculate_calories(food_t, q):
    res = 0.0
    l = 0
    
    def calculate_meal_calories(protein, fat, carbs, energy_kj, quantity):
        # Convert all inputs to float
        protein = to_float(protein)
        fat = to_float(fat)
        carbs = to_float(carbs)
        energy_kj = to_float(energy_kj)
        quantity = to_float(quantity)
        
        # Convert energy from kJ to kcal
        energy_kcal = energy_kj * 0.239
        
        protein *= quantity
        fat *= quantity
        carbs *= quantity
        energy_kcal *= quantity
        
        calories_from_protein = protein * 3
        calories_from_fat = fat * 7
        calories_from_carbs = carbs * 3
        
        return calories_from_protein + calories_from_fat + calories_from_carbs + energy_kcal
    
    for i in food_t:
        if not i.empty:
            f_cal = calculate_meal_calories(
                i.iloc[0, 0],  # protein
                i.iloc[0, 1],  # fat
                i.iloc[0, 2],  # carbs
                i.iloc[0, 3],  # energy (in kJ)
                q[l]           # quantity
            )
            res += f_cal
            l += 1
            
    return int(res)



def get_det_user(d):
    result = None
    try:
        # No need to connect to MySQL; MongoDB connection is used
        user = users_collection.find_one({"_id": ObjectId(d)})
        if user:
            result = {
                'height': user.get('height'),
                'weight': user.get('weight'),
                'age': user.get('age'),
                'gender': user.get('gender'),
                'activity_level': user.get('activity_level'),
                'email': user.get('email')
            }
    except Exception as e:
        st.error(f"Error: {e}")
    return result

def get_us_cat(d):
    result = None
    try:
        # No need to connect to MySQL; MongoDB connection is used
        user_goal = goals_collection.find_one({"user_id": d})
        if user_goal:
            result = user_goal.get('goal')
    except Exception as e:
        st.error(f"Error: {e}")
    return result

def send_email(user_email, total_calories, daily_caloric_goal):
    sender_email = "dietmanagement48@gmail.com"
    sender_password = "bqma bdxj nnja hgkd"
    subject = "Your Daily Caloric Summary-Reminder"
    
    # Create the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    
    body = f"""
    Hello,

    Here is your daily caloric summary:

    Total Calories Consumed: {total_calories}
    Daily Caloric Goal: {daily_caloric_goal}

    Keep up with your goals!

    Best,
    Your Diet App Team
    """
    
    message.attach(MIMEText(body, "plain"))
    
    # Send email using SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())
        server.close()
        st.success('Email sent successfully!')
    except Exception as e:
        st.error(f"Error sending email: {e}")

def diet(fp):
    col1, col2, col3 = st.columns(3)
    st.header('Welcome')
    user_id = st.session_state.current_user[1] 
    # st.title(user_id)# user_id is a string, not an integer

    res = verify_user_goal(user_id)
    # st.title(res);
    if res:
        st.subheader(f'Your Category: {res}')
        
        if st.button('Modify'):
            st.session_state.show_modify = True
        
        if 'show_modify' in st.session_state and st.session_state.show_modify:
            goal = st.selectbox('Weight Goal', ['Maintain Weight', 'Lose Weight', 'Gain Weight'])
            if st.button('Update'):
                goal_update(user_id, goal)
                st.session_state.show_modify = False
                st.session_state.current_page = 'diet'
                st.rerun()
        
        # Initialize session state lists if they do not exist
        if 'bk_list' not in st.session_state:
            st.session_state.bk_list = []
        if 'bkq_list' not in st.session_state:
            st.session_state.bkq_list = []
        if 'ln_list' not in st.session_state:
            st.session_state.ln_list = []
        if 'lnq_list' not in st.session_state:
            st.session_state.lnq_list = []
        if 'dn_list' not in st.session_state:
            st.session_state.dn_list = []
        if 'dnq_list' not in st.session_state:
            st.session_state.dnq_list = []

        data = pd.read_csv(fp)
        food_choices = data['Name'].unique().tolist()
        
        # Breakfast
        food_bk = st.selectbox('Enter Your Breakfast', options=food_choices)
        qbn = int(st.number_input('Enter the Quantity for Breakfast', format="%.0f"))
        qb = st.selectbox('BreakFast Quantity', ['Grams', 'Cups', 'Pieces'])
        if st.button('Add Breakfast'):
            if food_bk:
                st.session_state.bk_list.append(food_bk)
                st.session_state.bkq_list.append(qbn)
                st.success('Added')
        
        # Lunch
        food_ln = st.selectbox('Enter Your Lunch', options=food_choices)
        qln = int(st.number_input('Enter the Quantity for Lunch', format="%.0f"))
        ql = st.selectbox('Lunch Quantity', ['Grams', 'Cups', 'Pieces'])
        if st.button('Add Lunch'):
            if food_ln:
                st.session_state.ln_list.append(food_ln)
                st.session_state.lnq_list.append(qln)
                st.success('Added')
        
        # Dinner
        food_dn = st.selectbox('Enter Your Dinner', options=food_choices)
        qdn = int(st.number_input('Enter the Quantity for Dinner', format="%.0f"))
        qd = st.selectbox('Dinner Quantity', ['Grams', 'Cups', 'Pieces'])
        if st.button('Add Dinner'):
            if food_dn:
                st.session_state.dn_list.append(food_dn)
                st.session_state.dnq_list.append(qdn)
                st.success('Added')
        
        
        
        with col1:
            if st.button('Calculate'):
                rst1 = food_search(st.session_state.bk_list, data)
                rst2 = food_search(st.session_state.ln_list, data)
                rst3 = food_search(st.session_state.dn_list, data)
                
                if rst1 or rst2 or rst3:
                    res_det = get_det_user(user_id)
                    res_det_cat = get_us_cat(user_id)
                    rs1 = rs2 = rs3 = 0
                    if st.session_state.bkq_list:
                        rs1 = calculate_calories(rst1, st.session_state.bkq_list)
                    if st.session_state.lnq_list:
                        rs2 = calculate_calories(rst2, st.session_state.lnq_list)
                    if st.session_state.dnq_list:
                        rs3 = calculate_calories(rst3, st.session_state.dnq_list)
                    
                    total_calories = rs1 + rs2 + rs3
                    daily_caloric_goal = cal_daily(
                        res_det['height'],
                        res_det['weight'],
                        res_det['age'],
                        res_det['gender'],
                        res_det['activity_level'],
                        res_det_cat
                    )
                    
                    st.write(f'Total Calories Consumed: {total_calories}')
                    st.write(f'Daily Caloric Goal: {daily_caloric_goal}')
                    user_email = res_det['email']
                    send_email(user_email,total_calories,daily_caloric_goal)
                    users_collection.update_one(
                        { 'email':user_email },
                        { '$set': { 'last_update': ist_time } }
                    )
                                    
                else:
                    st.write('Food item not found. Please check the spelling or try another item.')
    else:
        goal = st.selectbox('Weight Goal', ['Maintain Weight', 'Lose Weight', 'Gain Weight'])
        if st.button('Submit'):
            goal_reg(user_id,goal)
            st.session_state.current_page = 'diet'
            st.rerun()
        
    with col2:
        if st.button('Clear'):
            st.session_state.bk_list = []
            st.session_state.bkq_list = []
            st.session_state.ln_list = []
            st.session_state.lnq_list = []
            st.session_state.dn_list = []
            st.session_state.dnq_list = []

    with col3:
        if st.button('Back'):
            st.session_state.current_page = 'h_main'
            st.rerun()

    if st.button('Logout'):
        st.session_state.bk_list = []
        st.session_state.bkq_list = []
        st.session_state.lnq_list = []
        st.session_state.ln_list = []
        st.session_state.dnq_list = []
        st.session_state.dn_list = []
        st.session_state.current_page = 'log'
        st.rerun()

def up_prof():
    inject_css()
    st.markdown('<h1 class="profile-update-title">Update Profile</h1>', unsafe_allow_html=True)

    with st.form(key='update_form', clear_on_submit=True):
        age = st.number_input('Age', min_value=0, max_value=120, step=1)
        height = st.number_input('Height (cm)', min_value=0.0, max_value=300.0, step=0.1, format='%f')
        weight = st.number_input('Weight (kg)', min_value=0.0, max_value=500.0, step=0.1, format='%f')
        act = st.selectbox('Activity Level', ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'])

        submit_button = st.form_submit_button('Submit', use_container_width=True)
        if submit_button:
            try:
                user_id = st.session_state.current_user[1]  # Assuming this is the ObjectId string
                result = users_collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {
                        "age": age,
                        "height": height,
                        "weight": weight,
                        "activity_level": act
                    }}
                )
                if result.modified_count > 0:
                    st.success('User details updated successfully!')
                else:
                    st.warning('No changes made.')
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button('Back'):
        st.session_state.current_page = 'h_main'
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def inject_css():
    with open('style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def main_1():
    inject_css()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'log'
   
    if st.session_state.current_page == 'log':
        log()
    elif st.session_state.current_page == 'reg':
        food_reg.reg()
    elif st.session_state.current_page == 'h_main':
        h_main()
    elif st.session_state.current_page == 'food_item':
        food_item('food.csv')
    elif st.session_state.current_page == 'diet':
        diet('food.csv')
    elif st.session_state.current_page == 'up_prof':
        up_prof()
    elif st.session_state.current_page == 'online_order':
        online_order()
   
    
    
   
        
    

    

