import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json


# ===============================
# CONNECT TO GOOGLE SHEETS
# ===============================
def get_client():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # ✅ STREAMLIT CLOUD (PRIMARY)
    if "gcp" in st.secrets:

        creds_dict = dict(st.secrets["gcp"])

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scope
        )

    # ✅ LOCAL FALLBACK
    else:

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json",
            scope
        )

    client = gspread.authorize(creds)

    return client


# ===============================
# LOAD SHEET
# ===============================
def load_sheet(sheet_name):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    return df


# ===============================
# UPDATE CELL
# ===============================
def update_cell(sheet_name, row, col, value):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    sheet.update_cell(row, col, value)
