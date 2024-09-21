import streamlit as st
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from datetime import datetime, timedelta
import os
import pdfplumber
import re
import pandas as pd
from fuzzywuzzy import process
def main():
    st.write("Welcome")

    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    user_id = 'me'
    today = datetime.utcnow().date()
    start_date = today
    end_date = today + timedelta(days=1)

    start_date_str = start_date.strftime('%Y/%m/%d')
    end_date_str = end_date.strftime('%Y/%m/%d')

    query = f'after:{start_date_str} before:{end_date_str}'

    messages = GMAIL.users().messages().list(userId=user_id, q=query).execute()
    mssg_list = messages.get('messages', [])
    final_list = []

    for mssg in mssg_list:
        m_id = mssg['id']
        message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
        payld = message['payload']
        headr = payld['headers']

        subject = None

        for one in headr:
            if one['name'] == 'Subject' and 'Zomato' in one['value']:
                subject = one['value']

        if subject and sender:
            if 'parts' in payld:
                for part in payld['parts']:
                    if part['filename'] and part['mimeType'] == 'application/pdf' and 'order_invoice' in part['filename'].lower():  # Check for PDF
                        attachment_id = part['body']['attachmentId']
                        attachment = GMAIL.users().messages().attachments().get(
                            userId=user_id, messageId=m_id, id=attachment_id
                        ).execute()

                        # Decode attachment
                        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                        
                        # Save PDF to a file
                        path = os.path.join("attachments", "food_det.pdf")
                        with open(path, 'wb') as f:
                            f.write(file_data)

                        st.write(f"Downloaded attachment: {part['filename']}")

    st.write("Completed PDF extraction!")

    # Function to extract food details from the PDF
    def extract_food_details_from_pdf(pdf_path):
        food_details = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                # Pattern to extract food details (Assume format "2 x Malai Meal")
                pattern = r"(\d+) x ([\w\s]+) (\d+ \d+ \d+)"
                matches = re.findall(pattern, text)

                for match in matches:
                    quantity = match[0]
                    food_name = match[1].strip()
                    food_details.append({'food_name': food_name, 'quantity': quantity})
        return food_details


    def to_float(value):
        try:
            return float(value)
        except ValueError:
            return 0.0

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

    # Path to your PDF and CSV
    pdf_path = "attachments/food_det.pdf"  # Path to the downloaded PDF

    # Extract food details from the PDF
    food_details_from_pdf = extract_food_details_from_pdf(pdf_path)

    # Match with calorie details from the CSV
    food_name_list=[]
    food_quantity=[]
    data = pd.read_csv("food.csv")
    for food in food_details_from_pdf:
        food_name_list.append(food['food_name'])
        food_quantity.append(food['quantity'])
        
    macron_det=food_search(food_name_list,data)
    res=calculate_calories(macron_det,food_quantity)
    rs=to_float(res)
    st.write(f'Total Calories:{res}')    



