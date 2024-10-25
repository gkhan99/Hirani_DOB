#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import yagmail

# Step 1: Fetch Data from the API
def fetch_dob_data():
    specific_date = datetime.now() - timedelta(days=3)
    formatted_date = specific_date.strftime("%m/%d/%Y")
    base_url = f"https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$where=issuance_date = '{formatted_date}'"
    
    try:
        response = requests.get(base_url)
        data = response.json()

        # Convert the response data to a DataFrame
        df = pd.DataFrame(data)
        
        if not df.empty:
            return df, specific_date
        else:
            print(f"No records found for {specific_date.strftime('%Y-%m-%d')}")
            return None, specific_date
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None, specific_date

# Step 2: Save Data to an Excel File
def save_data_to_excel(df, specific_date):
    filename = f"DOB_permits_data_{specific_date.strftime('%Y-%m-%d')}.xlsx"
    filepath = os.path.join(os.getcwd(), filename)
    
    try:
        df.to_excel(filepath, index=False)
        print(f"Data successfully saved to {filename}")
        return filepath
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return None

# Step 3: Send the Excel File via Email
def send_email_with_attachment(recipient_email, subject, body, attachment_path):
    try:
        # Set up yagmail with your Gmail and App Password
        yag = yagmail.SMTP('email@gmail.com', 'password')

        # Send the email
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body,
            attachments=attachment_path,
        )

        print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Step 4: Automation Workflow
def fetch_and_send_previous_day_data():
    # Fetch data for the specified date
    df, specific_date = fetch_dob_data()

    # If data is fetched, save it to an Excel file and send it via email
    if df is not None:
        excel_filename = save_data_to_excel(df, specific_date)
        if excel_filename:
            # Email details
            recipient_email = "marketing@hiranigroup.com"
            subject = f"DOB Permits Data for {specific_date.strftime('%Y-%m-%d')}"
            body = f"Please find attached the DOB Permits data for {specific_date.strftime('%Y-%m-%d')}."
            
            # Send the email with the Excel file attached
            send_email_with_attachment(recipient_email, subject, body, excel_filename)

# Run the function immediately (no need for scheduling)
fetch_and_send_previous_day_data()


# In[ ]:




