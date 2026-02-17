import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope (permissions)
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from credentials.json
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

# Authorize client
client = gspread.authorize(creds)


# Function to load sheet into pandas dataframe
def load_sheet(sheet_name):
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df


# Function to update pilot status
def update_pilot_status(sheet_name, pilot_name, new_status):
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()

    for i, row in enumerate(records):
        if row["name"] == pilot_name:
            sheet.update_cell(i+2, 6, new_status)
            return True

    return False
