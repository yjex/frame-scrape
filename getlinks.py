from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError
import pathlib
import pandas as pd
import gspread
import env

SERVICE_ACCOUNT_FILE = pathlib.Path().absolute().joinpath("credentials.json")
# print(SERVICE_ACCOUNT_FILE)
API_NAME = 'drive'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Ensure all files with links wanted are in this format: Campaign Name Format (e.g., 7.7 2024 Brand Name)
campaign = input("Campaign Name in 'Campaign Participation' format (e.g., 7.7 2024): ")
campaign_filter = "name contains "+"'"+campaign+"'"+" and name contains '.png'"

# print(campaign_filter)
# Call the Drive v3 API 
results = service.files().list(fields="files(name,webViewLink)", q=campaign_filter).execute()
items = results.get('files', [])
# print(results)

# Creating dataframe with first column for file name, second column for webViewLink
data = []
for row in items: 
    row_data = []
    row_data.append(row["name"])
    row_data.append(row["webViewLink"])
    data.append(row_data)

dataframe = pd.DataFrame(data, columns = ["name", "webViewLink"])
# print(dataframe)

# print(dataframe["name"])

keyword_link_dict = {}
for index, row in dataframe.iterrows():
    index_num = len(campaign)+1
    keyword_png = row["name"][index_num:]
    keyword_png = keyword_png.split(".")
    keyword = keyword_png[0]
    # print(keyword)
    # print(row["name"])
    # print(keyword)
    keyword_link_dict[keyword] = row["webViewLink"]

# print(keyword_link_dict)

