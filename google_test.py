import gspread
from google.oauth2.service_account import Credentials
from typing import List, Any

titles = ["Код_товару", "Назва_позиції", "Назва_позиції_укр", "Опис", "Опис_укр", "Ціна", "Оптова_ціна",
          "Валюта", "Одиниця_виміру", "Посилання_зображення", "Наявність", "Ярлик", "Тип_товару",
          "Мінімальне_замовлення_опт", "Номер_групи", "Назва_групи", "Унікальний_ідентифікатор", "Ідентифікатор_товару",
          "Ідентифікатор_групи"]

groups_titles = ["Номер_групи", "Назва_групи", "Назва_групи_укр", "Ідентифікатор_групи", "Номер_батьківської_групи",
                 "Ідентифікатор_батьківської_групи"]


def connect_table():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "12ryUt0S4LPl2u96h8K3pdV6qYSHU8ShaPPjzHbwkc-c"
    return client.open_by_key(sheet_id)


def write_to_google_sheet(name_sheet, data: List[List[Any]]):
    workbook = connect_table()
    sheet = workbook.worksheet(name_sheet)
    sheet.update("A2", data)


def get_all(name_sheet):
    workbook = connect_table()
    sheet = workbook.worksheet(name_sheet)
    data = sheet.get_all_values()
    filled_values_by_row = [[v for v in row if v] for row in data]
    filled_positions = [(r, c) for r, row in enumerate(data) for c, v in enumerate(row) if v]
    return filled_values_by_row[1:]
