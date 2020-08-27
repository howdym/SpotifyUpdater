import gspread
from oauth2client.service_account import ServiceAccountCredentials
import dataScraper
from gspread_formatting import *

# This is used to let Google know that we aren't accessing a document that we didn't have permission to edit.
"""Authentication"""
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets'
    , "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
key = "Get your API keys for Google Spreadsheet"
SpreadSheet = client.open_by_key(key)


def get_sheet_user(new_page_name):
    list_of_titles = [i.title for i in SpreadSheet.worksheets()]
    if new_page_name in list_of_titles:
        worksheet = SpreadSheet.worksheet(new_page_name)
        decision = input("Spreadsheet of name {} already exists. Continuing will erase all content in the spreadsheet. "
                         "Continue? [Y/N] ".format(new_page_name))
        if decision.lower() == "y":
            SpreadSheet.del_worksheet(worksheet=worksheet)
            worksheet = SpreadSheet.add_worksheet(title=new_page_name, rows="5", cols="5")

        else:
            print("Nothing Changed")
            return 0
    else:
        worksheet = SpreadSheet.add_worksheet(title=new_page_name, rows="5", cols="5")
    return worksheet


def get_sheet(new_page_name):
    worksheet = SpreadSheet.add_worksheet(title=new_page_name, rows="5", cols="5")
    return worksheet


def appearance_adjustments(worksheet):
    sheet_id = worksheet._properties['sheetId']
    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": 3
                    },
                    "properties": {
                        "pixelSize": 207
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    SpreadSheet.batch_update(body)

    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 35
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    SpreadSheet.batch_update(body)
    set_frozen(worksheet, 2, 3)


def add_first_row(data, worksheet):
    first_row = [v for k, v in data.first_row.items() if k != 'Entries']
    first_row.insert(0, "")
    first_row.insert(0, "Name (# of unique songs)")
    first_row.insert(0, data.first_row['Entries'])

    worksheet.append_row(first_row)


def add_second_row(data, worksheet):
    second_row = [k + " (" + str(v['Unique']) + ")" for k, v in data.dop.items()]
    second_row.insert(0, "Artist")
    second_row.insert(0, "Title")
    second_row.insert(0, "QTY")

    worksheet.append_row(second_row, table_range="A2")


def add_content(data, worksheet):
    content = []
    for i in data.sorted_lore_ids:
        entry = data.lore[i]
        row = list(entry['List'])
        for j in range(len(row)):
            if row[j] == 0:
                row[j] = ""
        row.insert(0, entry['Artists'])
        row.insert(0, entry['Name'])
        row.insert(0, entry['Sum'])
        content.append(row)

    worksheet.append_rows(content, table_range="A3")


def updater(new_page_name):
    worksheet = get_sheet(new_page_name)
    if worksheet == 0:
        return 1

    data = dataScraper.DataScraper()
    add_first_row(data, worksheet)
    add_second_row(data, worksheet)
    add_content(data, worksheet)

    appearance_adjustments(worksheet)
    return 0
