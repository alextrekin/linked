import gspread
from oauth2client.service_account import ServiceAccountCredentials
import consts as c

# Подсоединение к Google Таблицам
def connect_google_sheet():
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("google_api.json", scope)
    client = gspread.authorize(credentials)
    global sheet
    sheet = client.open(c.NAME_FILE).worksheet(c.NAME_SHEET_FILE)
# expected_headers = sheet.row_values(2)
# line_record = dict.fromkeys(expected_headers)
def search_profile():
    global sheet
    line_sheet = sheet.row_values(c.NUM_LINE)
    while line_sheet is not None:
        if len(line_sheet)<13:# тут отдаем имя фамилия и компания
            c.FIRST_NAME = line_sheet[0]
            c.LAST_NAME = line_sheet[1]
            c.COMPANY = line_sheet[2]
            c.LOCATION = line_sheet[8]
            c.NUM_LINE+=1
            line_sheet = sheet.row_values(c.NUM_LINE)
            return 
        else:
            c.NUM_LINE+=1
            line_sheet = sheet.row_values(c.NUM_LINE)
    c.END_DOCUMENT = True

def add_link(url):
    global sheet
    cell = 'M'+str(c.NUM_LINE-1)
    sheet.update(cell,url)