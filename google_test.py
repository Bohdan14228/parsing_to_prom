import gspread
from google.oauth2.service_account import Credentials

titles = ["Код_товару", "Назва_позиції", "Назва_позиції_укр", "Опис", "Опис_укр", "Ціна", "Оптова_ціна",
          "Валюта", "Одиниця_виміру", "Посилання_зображення", "Наявність", "Ярлик", "Тип_товару",
          "Мінімальне_замовлення_опт", "Номер_групи", "Назва_групи", "Унікальний_ідентифікатор", "Ідентифікатор_товару",
          "Ідентифікатор_групи"]

groups_titles = ["Номер_групи", "Назва_групи", "Назва_групи_укр", "Ідентифікатор_групи", "Номер_батьківської_групи",
                 "Ідентифікатор_батьківської_групи"]


def write_to_google_sheet(name_sheet, data=None):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "12ryUt0S4LPl2u96h8K3pdV6qYSHU8ShaPPjzHbwkc-c"
    workbook = client.open_by_key(sheet_id)
    if name_sheet in [i.title for i in workbook.worksheets()]:
        sheet_n = workbook.worksheet(name_sheet)
    else:
        sheet_n = workbook.add_worksheet(name_sheet, rows=3000, cols=200)
        sheet_n.update("A1", [titles])
        sheet_n.format("A1:S1", {"textFormat": {"bold": True}})
    sheet_n.update("A2", data)
