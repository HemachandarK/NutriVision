import streamlit as st

def home():
    # Embedding CSS with light green background
    st.markdown("""
    <style>
    body {
        background-color: #e8f5e9;  /* Light green background */
        font-family: 'Arial', sans-serif;
        color: #333;
    }
    
    h1 {
        font-size: 3em;
        color: #4CAF50;
        text-align: center;
        margin-top: 50px;
    }
    
    .overview-section {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        width: 80%;
        margin: 30px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .overview-section h2 {
        color: #333;
        font-size: 2em;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .overview-section p {
        font-size: 1.2em;
        line-height: 1.6;
        text-align: justify;
        color: #666;
    }

    .footer {
        text-align: center;
        padding: 20px;
        background-color: #4CAF50;
        color: white;
        margin-top: 50px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("NutriVision: Intelligent Food Recognition and Wellness Tracker")
    
    # Overview section
    st.markdown("""
    <div class="overview-section">
        <h2>About Our Nutrition App</h2>
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
    </div>
    """, unsafe_allow_html=True)


