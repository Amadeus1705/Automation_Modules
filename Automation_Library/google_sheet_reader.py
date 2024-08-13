percentage_format = {"type": "NUMBER","pattern": "0.00%"}
border_style = {
    'top': {'style': 'SOLID', 'color': {'red': 0, 'green': 0, 'blue': 0}},
    'bottom': {'style': 'SOLID', 'color': {'red': 0, 'green': 0, 'blue': 0}},
    'left': {'style': 'SOLID', 'color': {'red': 0, 'green': 0, 'blue': 0}},
    'right': {'style': 'SOLID', 'color': {'red': 0, 'green': 0, 'blue': 0}}
}

def format_requester(worksheet, start_row, end_row, start_column, end_column, cell_allignment, _format):
    if _format == border_style:
        d = {'userEnteredFormat': {'borders': border_style, "horizontalAlignment": cell_allignment,"verticalAlignment": "MIDDLE"}}
        s = 'userEnteredFormat.borders, userEnteredFormat.horizontalAlignment, userEnteredFormat.verticalAlignment'
    else:
        d = {"userEnteredFormat": {"numberFormat": _format,"horizontalAlignment": cell_allignment,"verticalAlignment": "MIDDLE"}}
        s = "userEnteredFormat.numberFormat, userEnteredFormat.horizontalAlignment, userEnteredFormat.verticalAlignment"
    r = {
        "repeatCell": {
            "range": {
                "sheetId": worksheet.id,
                "startRowIndex": start_row-1,
                "endRowIndex": end_row,
                "startColumnIndex": start_column-1,
                "endColumnIndex": end_column
            },
            "cell": d,
            "fields":s 
        }}
    return r


class GoogleSheetReader:
  def __init__(self, gsheet_key, service_account):
    self.gsheet_key = gsheet_key
    self.service_account = service_account
    self.gc = gspread.service_account_from_dict(service_account)


  def get_gsheet(self):
      return self.gc.open_by_key(self.gsheet_key)


  def get_sheet(self, worksheet_name):
      try:
          worksheet = self.get_gsheet().worksheet(worksheet_name)
      except gspread.exceptions.WorksheetNotFound:
          print('Worksheet not found')
          worksheet = self.get_gsheet().add_worksheet(title=worksheet_name, rows="200", cols="20")
      return worksheet


  def get_df_from_sheets(self, worksheet_name, range_=None):
      worksheet = self.get_sheet(worksheet_name)
      if range_ is None:
          df = pd.DataFrame(worksheet.get_all_records())
      else:
          df = pd.DataFrame(worksheet.get_values(range_))
          df.columns = df.iloc[0]
          df = df[1:]
      return df


  def set_df_in_sheets(self, worksheet_name, df, include_headers = True, row=1, col=1):
    try:
        worksheet = self.get_sheet(worksheet_name)
        if worksheet is None:
            worksheet = self.get_gsheet().add_worksheet(title=worksheet_name, rows="100", cols="20")
        set_with_dataframe(worksheet, df, row, col, include_column_header=include_headers)
        print(f"Data has been set to a {worksheet_name} sheet...")
        return True
    except Exception as e:
        print(e)
        return False
    
  def custom_set_df(self, sheet_name, df, header_include = True, row = 1, column = 1, percentage_list = [], round_list = [], cell_allignment = 'CENTER', border = False):
        for i in round_list:
            df[i] = np.round(df[i], 2)
        self.set_df_in_sheets(sheet_name, df, header_include, row, column)
        worksheet = self.get_sheet(sheet_name)
        requests = []
        for i, (column_name, column_data) in enumerate(df.iteritems()):
            max_length = max(max(df[column_name].astype(str).str.len()), len(str(column_name)))
            set_column_width(worksheet, f'{self.get_excel_cell(1, i+column)[:-1]}', ((max_length)*8)+8)
            if column_name in percentage_list:
                requests.append(format_requester(worksheet, row+1, row + len(df), i + column, i + column, cell_allignment, percentage_format))
        if border == True:
            requests.append(format_requester(worksheet, row, row + len(df), column, column + len(df.columns)-1, cell_allignment, border_style))
        
        if len(requests)!=0:
            worksheet.spreadsheet.batch_update({"requests": requests})
        worksheet.format(f"{self.get_excel_cell(row, column)}:{self.get_excel_cell(row, column+len(df.columns)-1)}", {"textFormat": {"bold": True},"horizontalAlignment": "CENTER","backgroundColor": {"red": 0.988, "green": 0.894, "blue": 0.839}})


  def get_excel_cell(self, row_num, col_num):
      col_str = ""
      div = col_num
      while div:
          modulo = (div - 1) % 26
          col_str = chr(65 + modulo) + col_str
          div = (div - 1) // 26
      return col_str + str(row_num)

  
  def clear_sheets(self, sheetname, start_row, start_column):
      sheet = self.get_sheet(sheetname)
      data_range = sheet.get_all_values()
      num_rows = len(data_range)
      num_cols = len(data_range[0])
      range_ = '{start}:{end}'.format(start=self.get_excel_cell(start_row, start_column),
                                      end=self.get_excel_cell(num_rows, num_cols))
      print(range_)
      sheet.batch_clear([range_])
