import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ============================
# CONNECT USING STREAMLIT SECRETS
# ============================

def get_client():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = st.secrets["gcp_service_account"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope
    )

    client = gspread.authorize(creds)

    return client


# ============================
# LOAD SHEET FUNCTION
# ============================

def load_sheet(sheet_name):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    return df
