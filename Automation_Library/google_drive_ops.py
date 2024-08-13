class GoogleDriveOps:
    def __init__(self, creds, scope: Optional[List[str]] = None):
        self.creds = creds
        self.scope = scope or ['https://www.googleapis.com/auth/drive.appdata',
                               'https://www.googleapis.com/auth/drive']
        self.gauth = self.get_credentials()
        self.drive = GoogleDrive(self.gauth)


    def get_credentials(self):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.creds, self.scope)
        return gauth


    def get_folder_dict(self, folder_id):

        """
        Returns: List of folder dictionaries
        - Get all the folders within a specific parent folder.
        Parameters:
        - parent_folder_id [str]: The ID of the parent folder you want to list folders within.
        """

        query = "'{}' in parents and trashed=false".format(folder_id)
        file_list = self.drive.ListFile({'q': query}).GetList()
        folder_dict = {}
        for file in file_list:
            folder_dict[file['title']] = file['id']
        return folder_dict



    def get_all_folders_in_folder(self, parent_folder_id):

        """
        Returns: List of folder dictionaries
        - Get all the folders within a specific parent folder.
        Parameters:
        - parent_folder_id [str]: The ID of the parent folder you want to list folders within.
        """


        query = "'{}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        query = query.format(parent_folder_id)
        file_list = self.drive.ListFile({'q': query}).GetList()

        folder_list = []
        for file in file_list:
            folder_info = {
                'title': file['title'],
                'id': file['id']
            }
            folder_list.append(folder_info)

        return folder_list
      
    def Create_folder(self , folder_name , parent_folder_id):
      """

      Returns: Dictionary
      Get all the folder Id's as dictionary. 
      Authorize G-Drive Credentials before using Create_folder function. Use the following method to authorize credentials.

        {gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_key, SCOPES)
        drive = GoogleDrive(gauth)}

      """
      files_present = self.get_folder_dict(parent_folder_id)
      if folder_name not in files_present.keys():

        folder = self.drive.CreateFile({'parents':[{'id': parent_folder_id}],'title':folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        folder_created =  self.get_folder_dict(parent_folder_id)
      else:
        print('Folder with same name already exists. Please try with another name')
        folder_created =  self.get_folder_dict(parent_folder_id)
      return folder_created
    



    def Create_file(self, folder_id, title):
      """
      Create a Google Sheets spreadsheet in a Google Drive folder.

      Parameters:
      - folder_id: The ID of the Google Drive folder where you want to create the spreadsheet.
      - title: The title (name) for the new spreadsheet.

      Note: The 'drive' variable and required modules should be imported and available in the same scope where this function is called.
      """
      
      # Create a new Google Sheets file in the specified folder
      spreadsheet = self.drive.CreateFile(
          {
              "parents": [{"id": folder_id}],
              "title": title,
              "mimeType": "application/vnd.google-apps.spreadsheet",
          }
      )

      # Upload the empty spreadsheet
      spreadsheet.Upload()

      print(f"Created Google Sheets file: '{title}' in folder with ID '{folder_id}'")

    def convert_to_pdf(self, template_id: str, folder_id: str, title: str) -> bool:
        '''
        Converts excel template into pdf and uploads it to the given G-Drive folder.
        Parameters:
        - template_id: The ID of the Google Sheets template file.
        - folder_id: The ID of the Google Drive folder where the PDF will be stored.
        - title: The title (name) for the PDF file.
        '''
        file_obj = self.drive.CreateFile({'id': template_id})
        local_pdf_path = os.path.join(os.getcwd(), f'{title}.pdf')
        file_obj.GetContentFile(local_pdf_path, mimetype='application/pdf')
        
        gfile = self.drive.CreateFile({'parents': [{'id': folder_id}], 'title': f'{title}.pdf'})
        gfile.SetContentFile(local_pdf_path)
        gfile.Upload()
        
        os.remove(local_pdf_path)
        return True
