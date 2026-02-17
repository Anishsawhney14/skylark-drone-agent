import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def get_client():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load credentials from Streamlit Secrets
    creds_dict = dict(st.secrets["gcp"])

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    client = gspread.authorize(creds)

    return client


def load_sheet(sheet_name):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    data = sheet.get_all_records()

    return pd.DataFrame(data)


def update_sheet(sheet_name, df):

    client = get_client()

    sheet = client.open(sheet_name).sheet1

    sheet.clear()

    sheet.update([df.columns.values.tolist()] + df.values.tolist())
