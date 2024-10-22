import streamlit as st
from streamlit_scroll_navigation import scroll_navbar
from pymongo import MongoClient
from food_log import main_1
from streamlitimage import findimage
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import threading
import time


def home():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.food_det_db
    users_collection = db.user_details
    anchor_ids = ["About", "Features", "Nutrient", "Login", "Contact"]
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Aldrich&display=swap');
            * {
                margin: 0;
                padding: 0;
                list-style-type: none;
            }
            body {
                font-family:Aldrich;
                background: #4CAF50;  /* Main background color */
                color: #fff;  /* White text color */
            }
            
            h2, h3, h4, h5, h6 {
                font-family:Aldrich;  /* Target all header tags */
                color:#800080;  /* Highlight color for section headers */
                font-size: 28px; /* Increase subheader font size */
            }

            p {
                font-family:Aldrich;
                color: #140D18;  /* Color for paragraph text */
                font-size: 20px; /* Increase paragraph font size */
            }

            /* Center align features text */
            .features-container {
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

        </style>
    """, unsafe_allow_html=True)

    # Scrollable navigation bar
    scroll_navbar(
        anchor_ids=anchor_ids,
        key="navbar4",
        orientation="horizontal",
        override_styles={
            "navbarButtonBase": {
                "font-family":"Aldrich",
                "backgroundColor": "white",  # White background
                "color": "#111011",  # Purple text color
                "fontSize": "14px",  # Smaller font size
                "padding": "8px 12px",  # Reduced padding for smaller button size
                "borderRadius": "10px",  # Rounded corners for buttons
                "border": "2px solid #800080",  # Purple border
            },
            "navbarButtonHover": {
                "font-family":"Aldrich",
                "backgroundColor": "#dedcff",  # Light green background on hover
                "color": "#111011",  # Dark green text color on hover
            },
            "navigationBarBase": {
                "font-family":"Aldrich",
                "backgroundColor": "#ffffff",  # White background for the navbar
                "padding": "5px",  # Reduced padding for the navbar
                "borderRadius": "10px",  # Rounded corners for navbar
                "boxShadow": "0 2px 5px rgba(0, 0, 0, 0.2)",  # Slight shadow for depth
            }
        }
    )


    st.subheader("About", anchor="About")
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <p>
                Our Nutrition App is designed to help you maintain a healthy diet effortlessly. 
                With our app, you can upload images of your food to quickly identify the number 
                of calories and get detailed nutritional information. Our goal is to make 
                nutrition tracking easy, fun, and accessible for everyone.
            </p>
            <p>
                In addition to tracking your calories, we also provide insights into food-related 
                diseases. Based on your diet and health conditions, our app offers personalized tips 
                and dietary recommendations to support a healthier lifestyle. 
            </p>
            <p>
                Whether you're trying to lose weight, manage a medical condition, or simply eat healthier, 
                our Nutrition App is here to support you every step of the way. Start your journey towards 
                better health with us today!
            </p>
            <br>
        </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.subheader("Features", anchor="Features")
    st.markdown("""
        <style>
            .feature-box {
                background-color: #ffffff; /* White background */
                color: #008000; /* Text color */
                border: 2px solid #800080; /* Purple border */
                border-radius: 15px; /* Rounded corners */
                padding: 20px; /* Internal spacing */
                text-align: center; /* Center text */
                flex: 1; /* Equal space for all boxes */
                margin: 0 10px; /* Space between boxes */
                transition: background-color 0.3s; /* Smooth transition for hover */
            }
            .feature-box:hover {
                background-color: #dedcff; /* Light green on hover */
            }
        </style>
        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div class="feature-box">
                <p>Realtime food nutrient analysis</p>
            </div>
            <div class="feature-box">
                <p>Diet management</p>
            </div>
            <div class="feature-box">
                <p>Disease details</p>
            </div>
            <br>
            <br>
        </div>
    """, unsafe_allow_html=True)


    st.subheader("RealTime nutrient Analysis", anchor="Nutrient")
    findimage()

    # Login Section
    st.subheader("Login", anchor="Login")
    main_1()

    st.subheader("Contact", anchor="Contact")
    st.markdown("""
        <div style="margin-bottom: 20px; 
                    background: #ffffff; 
                    color: #008000; 
                    text-align: center; 
                    padding: 20px; 
                    border: 2px solid #800080; 
                    border-radius: 15px;">  
            <p>
                If you have any questions or feedback, feel free to reach out to us:
            </p>
            <div>
                <p><strong>Name:</strong> Your Name</p>
                <p><strong>Email:</strong> your.email@example.com</p>
                <p><strong>Message:</strong> Your Message</p>
            </div>
            <br>
        </div>
    """, unsafe_allow_html=True)


    def send_email(to_email, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = "dietmanagement48@gmail.com"
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("dietmanagement48@gmail.com", "bqma bdxj nnja hgkd")
            server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Reminder Check Function
    def check_updates_and_send_emails():
        while True:
            current_time = datetime.utcnow()
            breakfast_deadline = current_time.replace(hour=10, minute=50, second=0, microsecond=0)
            lunch_deadline = current_time.replace(hour=15, minute=0, second=0, microsecond=0)
            dinner_deadline = current_time.replace(hour=20, minute=0, second=0, microsecond=0)

            users = users_collection.find()

            for user in users:
                last_update = user['last_update']
                email = user['email']
                if last_update:
                    time_since_last_update = current_time - last_update

                    # Check for breakfast reminder
                    if current_time < breakfast_deadline and time_since_last_update > timedelta(hours=3):
                        send_email(email, "Breakfast Reminder", "Please update your breakfast details.")

                    # Check for lunch reminder
                    if current_time >= breakfast_deadline and current_time < lunch_deadline and time_since_last_update > timedelta(hours=5):
                        send_email(email, "Lunch Reminder", "Please update your lunch details.")

                    # Check for dinner reminder
                    if current_time >= lunch_deadline and current_time < dinner_deadline and time_since_last_update > timedelta(hours=5):
                        send_email(email, "Dinner Reminder", "Please update your dinner details.")

            # Sleep for a while before checking again
            time.sleep(3600)  # Check every hour

    # Start the reminder thread
    reminder_thread = threading.Thread(target=check_updates_and_send_emails)
    reminder_thread.start()


home()