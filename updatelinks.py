import gspread
import pandas as pd
import env
import pathlib
import getlinks

filepath = pathlib.Path().absolute().joinpath("credentials.json")

gc = gspread.service_account(filename=filepath)

workbook = gc.open(env.workbook_name)

sheet = workbook.worksheet(env.tab_name)

def find_row(sheet, search_value):
    all_req = sheet.get_all_values()

    for row_idx, row in enumerate(all_req, start=1):
        if search_value in row:
            return row_idx
        
    return None

# Creating Dataframe
sheet_df = pd.DataFrame(sheet.get_all_values()[2:])
# print(sheet_df)

# Creating Dataframe with Campaign Filter
filtered_df = sheet_df[sheet_df[7] == getlinks.campaign]
# print(filtered_df)

filtered_dict = dict(zip(filtered_df[2], filtered_df[0]))
# print(filtered_dict)

not_updated = []

for element in filtered_dict:
    for keyword in getlinks.keyword_link_dict:
        if keyword.lower() in element.lower():
            # print(keyword)
            # print(element)
            row_num = find_row(sheet, filtered_dict[element])
            # print(row_num)
            if sheet.cell(row_num, 28).value == None:
                sheet.update_cell(row_num, 28, getlinks.keyword_link_dict[keyword])

print(env.final_note)