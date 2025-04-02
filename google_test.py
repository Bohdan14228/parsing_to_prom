import gspread
from google.oauth2.service_account import Credentials
from typing import List, Any

titles = ["Код_товару", "Назва_позиції", "Назва_позиції_укр", "Опис", "Опис_укр", "Ціна", "Оптова_ціна",
          "Валюта", "Одиниця_виміру", "Посилання_зображення", "Наявність", "Ярлик", "Тип_товару",
          "Мінімальне_замовлення_опт", "Номер_групи", "Назва_групи", "Унікальний_ідентифікатор", "Ідентифікатор_товару",
          "Ідентифікатор_групи"]

groups_titles = ["Номер_групи", "Назва_групи", "Назва_групи_укр", "Ідентифікатор_групи", "Номер_батьківської_групи",
                 "Ідентифікатор_батьківської_групи"]


def write_to_google_sheet(name_sheet, data: List[List[Any]]):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "12ryUt0S4LPl2u96h8K3pdV6qYSHU8ShaPPjzHbwkc-c"
    workbook = client.open_by_key(sheet_id)

    sheet_n = workbook.worksheet(name_sheet)
    sheet_n.update("A2", data)
