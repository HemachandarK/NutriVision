# NutriVision – A Nutrition and Health Management System

NutriVision is a comprehensive nutrition and wellness management application that enables users to track their dietary intake, predict potential health risks, and receive personalized diet suggestions. The system integrates computer vision, email processing, machine learning, and health analytics into one cohesive platform.

## Features

- **Food Recognition via Image Upload**  
  Uses a pre-trained InceptionV3 model to identify food items from images and provide nutritional breakdown, including calories, proteins, carbohydrates, and fats.

- **Gmail Order Extraction**  
  Automatically reads food order details from services like Zomato or Swiggy using the Gmail API, helping users track their calorie intake without manual input.

- **Dietary Management Dashboard**  
  An interactive Streamlit dashboard where users can:
  - Set personal dietary goals (e.g., weight gain or loss)
  - Monitor current calorie intake
  - Get food suggestions based on dietary preferences and health objectives

- **Disease Prediction Module**  
  Predicts potential diseases based on user health data and dietary history. Offers tailored diet plans to help mitigate risk.

- **Search History-Based Recommendations**  
  Uses a recommendation system to suggest meals based on user preferences and past search behavior.

- **Email Notifications**  
  Sends automated reminders to users who miss meals or do not meet their calorie targets throughout the day.

## Tech Stack

| Component        | Technology                           |
|------------------|---------------------------------------|
| Frontend         | Streamlit                             |
| Backend          | Python, Flask (Gmail API integration) |
| Machine Learning | InceptionV3 (TensorFlow), Scikit-learn|
| Database         | MongoDB                               |
| Email Access     | Gmail API                             |
| Image Handling   | PIL, OpenCV                           |

## Architecture Overview

1. User uploads an image or food order is fetched from Gmail.
2. The food item is classified using a deep learning model.
3. Macronutrient information is retrieved and logged.
4. User’s diet history is updated and shown on the dashboard.
5. Based on intake and goals, recommendations or alerts are generated.
