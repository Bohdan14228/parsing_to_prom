import gspread
from google.oauth2.service_account import Credentials

titles = ["Код_товару", "Назва_позиції", "Назва_позиції_укр", "Опис", "Опис_укр", "Ціна", "Оптова_ціна",
          "Валюта", "Одиниця_виміру", "Посилання_зображення", "Наявність", "Ярлик", "Тип_товару",
          "Мінімальне_замовлення_опт", "Номер_групи", "Назва_групи", "Унікальний_ідентифікатор", "Ідентифікатор_товару",
          "Ідентифікатор_групи"]


def write_to_google_sheet(name_sheet, data=[[]]):
    if data is None:
        data = titles
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "12ryUt0S4LPl2u96h8K3pdV6qYSHU8ShaPPjzHbwkc-c"
    workbook = client.open_by_key(sheet_id)
    # name_sheet = 'Products'
    if name_sheet in [i.title for i in workbook.worksheets()]:
        sheet_n = workbook.worksheet(name_sheet)
    else:
        sheet_n = workbook.add_worksheet(name_sheet, rows=3000, cols=200)
        sheet_n.update("A1", [data])
        sheet_n.format("A1:S1", {"textFormat": {"bold": True}})
    sheet_n.update("A2", data)

write_to_google_sheet("Products")

    # sheet_n.update(f"A1:C{len(values)}", values)
    # sheet_n.update_cell(len(values) + 1, 2, "=sum(B2:B4)")
    # sheet_n.update_cell(len(values) + 1, 3, "=sum(C2:C4)")
    # sheet_n.format("A1:C1", {"textFormat": {"bold": True}})

"""Выводим первый ряд из первой таблицы"""
# values_list = workbook.sheet1.row_values(1)
# print(values_list)

"""Выводим список таблиц"""
# sheets = map(lambda x: x.title, workbook.worksheets())
# print(list(sheets) )
# sheets = [i.title for i in workbook.worksheets()]
# print(sheets)


# работа с одной табличкой
# sheet = workbook.worksheet("Products")  # workbook.sheet1
# sheet.update_title("Hello world")   # обновляем имя выбранной таблицы
# sheet.update_acell("A1", 1)    # обновление ячеек
# sheet.update_cell(6, 1, "Hello World")     # обновление ячейки по ряду и колонке

# value = sheet.acell("A1").value     # выводит значение в ячейке
# print(value)

# if not sheet.acell('A7').value:
#     sheet.update_acell("A7", "NEW")

# cell_find = sheet.find('NEW')
# print(cell_find.row, cell_find.col)

# sheet.format("A2", {"textFormat": {"bold": True}})  # если есть текст в ячейке делает его жирным

# new_name = "Basket"
# if new_name in [i.title for i in workbook.worksheets()]:
#     sheet_n = workbook.worksheet(new_name)
# else:
#     sheet_n = workbook.add_worksheet(new_name, rows=10, cols=10)
# values = [
#     ["Name", "Price", "Quantity"],
#     ["Basketball", 29.99, 1],
#     ["Jeans", 39.99, 4],
#     ["Soup", 7.99, 3]
# ]
# sheet_n.clear()
# sheet_n.update(f"A1:C{len(values)}", values)
# sheet_n.update_cell(len(values) + 1, 2, "=sum(B2:B4)")
# sheet_n.update_cell(len(values) + 1, 3, "=sum(C2:C4)")
# sheet_n.format("A1:C1", {"textFormat": {"bold": True}})
