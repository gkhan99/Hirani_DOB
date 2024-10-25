#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import yagmail

def fetch_and_send_previous_day_data():
    # Calculate the previous day's date
    previous_day = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    # Base URL for the previous day
    base_url = f"https://data.cityofnewyork.us/resource/rbx6-tga4.json?$where=issued_date >= '{previous_day}T00:00:00' AND issued_date < '{previous_day}T23:59:59'"
    
    try:
        # Fetching the data
        response = requests.get(base_url)
        data = response.json()

        # Converting the data into a pandas DataFrame
        df = pd.DataFrame(data)

        # If 'issued_date' exists, process and save
        if 'issued_date' in df.columns:
            df['issued_date'] = pd.to_datetime(df['issued_date'], errors='coerce')
            df['modified_issued_date'] = df['issued_date'].dt.date
            df = df[['modified_issued_date'] + [col for col in df.columns if col != 'modified_issued_date']]

            # Save the Excel file in the current folder
            filename = f"NYC_DOB_NOW_{previous_day}.xlsx"
            filepath = os.path.join(os.getcwd(), filename)
            df.to_excel(filepath, index=False)

            # Send email with the Excel file as attachment
            recipient_email = "marketing@hiranigroup.com"
            subject = f"NYC DOB Data for {previous_day}"
            body = f"Hey, please find all issued permits from DOB NOW for {previous_day}"
            yag = yagmail.SMTP('email@gmail.com', 'password')  # Replace with your Gmail and app password
            yag.send(to=recipient_email, subject=subject, contents=body, attachments=filepath)

            print(f"Data for {previous_day} saved to {filename} and email sent to {recipient_email}")
        else:
            print(f"No 'issued_date' data available for {previous_day}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function immediately (no need for scheduling)
fetch_and_send_previous_day_data()


# In[ ]:




