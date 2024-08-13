class GoogleDocsReader:
    def __init__(self, creds):
        self.creds = creds
        self.service = self.build_service()

    def build_service(self):
        scopes = ['https://www.googleapis.com/auth/documents']
        creds_obj = service_account.Credentials.from_service_account_info(self.creds, scopes=scopes)
        service = build('docs', 'v1', credentials=creds_obj)
        return service

    def read_document_metadata(self, document_id):
        document = self.service.documents().get(documentId=document_id).execute()
        return document
      
    def read_doc_content(self, document_id):
      document_content = self.read_document_metadata(document_id)
      tst = []
      try:
          for i in document_content.get('body').get('content'):
              j = i.get('paragraph')
              if j != None:
                  k = j.get('elements')
                  tst.append(k[0].get('textRun').get('content'))     
      except:
          pass
      content = ' '.join(tst)
      return content