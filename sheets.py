import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os


# ================================
# GOOGLE SHEETS CLIENT CONNECTION
# ================================

def get_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = None

    # ------------------------------
    # Try Streamlit Cloud Secrets
    # ------------------------------
    try:
        creds_dict = dict(st.secrets["gcp"])

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scope
        )

    except Exception:

        # ------------------------------
        # Fallback for Local Development
        # ------------------------------
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json",
            scope
        )

    client = gspread.authorize(creds)

    return client


# ================================
# LOAD GOOGLE SHEET INTO DATAFRAME
# ================================

def load_sheet(sheet_name):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    data = sheet.get_all_records()

    df = pd.DataFrame(data)

    return df


# ================================
# UPDATE CELL FUNCTION (OPTIONAL)
# ================================

def update_cell(sheet_name, row, col, value):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    sheet.update_cell(row, col, value)


# ================================
# UPDATE ROW BY COLUMN VALUE
# ================================

def update_by_id(sheet_name, id_column, id_value, updates_dict):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    records = sheet.get_all_records()

    headers = sheet.row_values(1)

    for i, row in enumerate(records):

        if str(row[id_column]) == str(id_value):

            for column_name, new_value in updates_dict.items():

                col_index = headers.index(column_name) + 1

                sheet.update_cell(i + 2, col_index, new_value)

            return True

    return False
