import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import io
import requests
import pandas as pd
import plotly.express as px

# Initialize session state variables
def findimage():
    if 'option' not in st.session_state:
        st.session_state.option = None
    if 'show_upload' not in st.session_state:
        st.session_state.show_upload = False
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("Know your food, nutrient details ...")

    with col2:
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📁"):
                st.session_state.option = "Upload Image"
                st.session_state.show_upload = not st.session_state.show_upload
                st.session_state.show_camera = False  # Hide camera option when toggling
        with col4:
            if st.button("📷"):
                st.session_state.option = "Take a Picture"
                st.session_state.show_camera = not st.session_state.show_camera
                st.session_state.show_upload = False  # Hide upload option when toggling

    # Display the appropriate input based on the selection
    uploaded_image = None

    if st.session_state.option == "Upload Image" and st.session_state.show_upload:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True, width=300)
            st.success("Image uploaded successfully!")

    if st.session_state.option == "Take a Picture" and st.session_state.show_camera:
        camera_input = st.camera_input("Or take a picture")
        if camera_input:
            uploaded_image = Image.open(io.BytesIO(camera_input.getvalue()))
            st.image(uploaded_image, caption="Captured Image", use_column_width=True, width=300)
            st.success("Image captured successfully!")

    model_path = "./model_inceptionV3.h5"
    # st.write("Loading the model...")
    model = load_model(model_path)
    # st.write("Done!")

    category = {
        0: ['boiled egg', 'boiled egg'], 1: ['burger', 'burger'], 2: ['chapati', 'chapati'],
        3: ['chole_bhature', 'Chole Bhature'], 4: ['curd rice', 'curd rice'],
        5: ['fish fry', 'fish fry'], 6: ['fried_rice', 'Fried Rice'], 7: ['idli', 'Idli'], 8: ['kadai_paneer', 'Kadai Paneer'],
        9: ['lemon rice', 'lemon rice'],
        10: ['masala_dosa', 'Dosa'], 11: ['noodles', 'noodles'], 12: ['parotta', 'parotta'],
        13: ['sambar', 'sambar'], 14: ['white rice', 'white rice']
    }

    def predict_image(img, model):
        img = img.resize((299, 299))
        img_array = image.img_to_array(img)
        img_processed = np.expand_dims(img_array, axis=0)
        img_processed /= 255.

        prediction = model.predict(img_processed)
        index = np.argmax(prediction)
        return category[index][1]

    # Text input for manual food name entry
    manual_food_name = st.text_input("Enter food name for nutrient details:")

    if uploaded_image is not None:
        food_name = predict_image(uploaded_image, model)
        st.write(f"Prediction: {food_name}")

    # Use the predicted food name or manual input food name
    final_food_name = manual_food_name if manual_food_name else (food_name if uploaded_image is not None else None)

    if final_food_name:
        st.title("KNOW YOUR FOOD CALORIE...")

        # API request for nutrient details
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        response = requests.get(api_url + final_food_name, headers={'X-Api-Key': 'rOwKaN/PhGM/uQ3ApeqHLQ==fBG4stdHXc65xy2U'})

        if response.status_code == 200:
            data = response.json()
            item = data['items'][0]

            st.title(f"Nutrition Information for {item['name']}")

            nutrient_labels = ['calories', 'fat_total_g', 'fat_saturated_g', 'protein_g', 'sodium_mg', 'potassium_mg', 'cholesterol_mg', 'carbohydrates_total_g', 'fiber_g', 'sugar_g']
            nutrient_values = [item[nutrient] for nutrient in nutrient_labels]

            # Display in Table
            df = pd.DataFrame({
                'Nutrient': nutrient_labels,
                'Value': nutrient_values
            })
            st.write("### Nutrient Table")
            st.dataframe(df)

            # Pie Chart
            fig = px.pie(df, names='Nutrient', values='Value', title='Nutrient Distribution')
            st.plotly_chart(fig)

        else:
            st.write("Error:", response.status_code, response.text)
