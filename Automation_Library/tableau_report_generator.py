class Tableau_report_generator():


    def __init__(self):

        tableau_config = {
        'tableau_prod': {
        'server': "https://tableau.dp.navi-tech.in/" ,
        'api_version': '3.15',
        'username': '',
        'password': '',
        'site_name': '',
        'site_url': '',
                        }
        }

        # create Tableau Server connection object
        self.conn = TableauServerConnection(tableau_config, env='tableau_prod')
        # sign in to the Tableau Server connection
        self.conn.sign_in()
        print('Connected to https://tableau.dp.navi-tech.in/')
        
    # @property
    def get_view_id(self, view_name, workbook_name):
        
        try:
            views_df = querying.get_views_dataframe(self.conn)
            wb_unnest_df = flatten_dict_column(df = views_df,keys=['name','id'], col_name='workbook')
            result_df = wb_unnest_df.loc[(wb_unnest_df['name']== view_name) & (wb_unnest_df['workbook_name']==workbook_name)]
            if len(result_df) == 0:
                print('View not found. Verify the workbook name and view name')
            else:
                view_id = result_df.id.values[0]
        except Exception as e:
            print('Exception Error: ', e)
        return view_id
    
    def get_all_views(self, workbook_name):
        
        try:
            views_df = querying.get_views_dataframe(self.conn)
            wb_unnest_df = flatten_dict_column(df = views_df,keys=['name','id'], col_name='workbook')
            result_df = wb_unnest_df.loc[(wb_unnest_df['workbook_name']==workbook_name)]
            if len(result_df) == 0:
                print('View not found. Verify the workbook name and view name')
            else:
                view_dct = {}
                for row in result_df.iterrows():
                    view_dct[row[1][5]] = row[1][4]
        except Exception as e:
            print('Exception Error: ', e)
        return view_dct
    
    # @property
    def get_view_csv(self, view_name : str ,workbook_name : str, path : Optional[str] = None):
        """
        Download csv of the backend data of tableau view.

        Parameters:
        - view_name (str): The name of the view to retrieve.
        - workbook_name (str): The name of the workbook containing the view.
        - path (str, optional): The path to save the downloaded csv.

        Returns:
        - str: The path to the downloaded image.
        """

        view_id = self.get_view_id(view_name , workbook_name)
        if not path:
            download_path = f'/dbfs/FileStore/{view_name}.csv'
        else:
            download_path = f'{path}/{view_name}.csv'
        view_response = self.conn.query_view_data(view_id)
        with open(download_path , 'wb') as file:
            file.write(view_response.content)
        return download_path
    
    # @property
    def get_view_df(self, view_name ,workbook_name):
        download_path = self.get_view_csv(view_name ,workbook_name)
        df = pd.read_csv(download_path)
        os.remove(download_path)
        return df
    

    def _apply_custom_filters(self, filters: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Apply custom filters to be used in querying a view image.

        Parameters:
        - filters (Dict[str, List[str]]): A dictionary where each key is the filter name
                                          and the corresponding value is a list of filter values.

        Returns:
        - Dict[str, str]: A dictionary where each key is the filter name (with necessary encoding)
                          and the corresponding value is the encoded filter values concatenated as a string.
        """
        encoded_filters = {}
        for filter_name, filter_values in filters.items():
            # Encode filter name
            encoded_filter_name = urllib.parse.quote(filter_name)
            # Encode filter values and join them with ","
            # encoded_filter_values = ",".join(urllib.parse.quote(value) for value in filter_values)
            encoded_filter_values = ",".join(urllib.parse.quote(str(value).lower() if isinstance(value, bool) else str(value)) for value in filter_values)
            
            # Construct filter expression
            filter_expression = f"vf_{encoded_filter_name}={encoded_filter_values}"
            # Add to encoded_filters dictionary
            encoded_filters[filter_name] = filter_expression
        return encoded_filters
    

    # @property
    def download_view_image(self,
                        view_name : str,
                        workbook_name : str,
                        path : Optional[str] = None,
                        filters: Optional[Dict[str, List[str]]] = None
                        ):
        
        """
        Retrieve an image of a specific view.

        Parameters:
        - view_name (str): The name of the view to retrieve.
        - workbook_name (str): The name of the workbook containing the view.
        - path (str, optional): The path to save the downloaded image.
                                If not provided, the default path will be used.
        - filters (dict, optional): The name of the filter and values to apply to the view.

        Returns:
        - str: The path to the downloaded image.
        """
        if filters:
            encoded_filters = self._apply_custom_filters(filters)
        else:
            encoded_filters = None
        view_id = self.get_view_id(view_name , workbook_name)
        
        if not path:
            download_path = f'/dbfs/FileStore/{view_name}.png'
        else:
            download_path = f'{path}/{view_name}.png'
            
        view_img_response = self.conn.query_view_image(view_id, parameter_dict=encoded_filters)
        with open(download_path , 'wb') as file:
            file.write(view_img_response.content)
        print(f'Image saved: {download_path}')
        with open(download_path, "rb") as f:
            image = Image.open(io.BytesIO(f.read()))
        return image
    
    def download_view_pdf(self,
                        view_name : str,
                        workbook_name : str,
                        path : Optional[str] = None,
                        filters: Optional[Dict[str, List[str]]] = None
                        ):
        
        """
        Retrieve an image of a specific view.

        Parameters:
        - view_name (str): The name of the view to retrieve.
        - workbook_name (str): The name of the workbook containing the view.
        - path (str, optional): The path to save the downloaded image.
                                If not provided, the default path will be used.
        - filters (dict, optional): The name of the filter and values to apply to the view.

        Returns:
        - str: The path to the downloaded image.
        """
        if filters:
            encoded_filters = self._apply_custom_filters(filters)
        else:
            encoded_filters = None
        view_id = self.get_view_id(view_name , workbook_name)
        
        if not path:
            download_path = f'/dbfs/FileStore/{view_name}.pdf'
        else:
            download_path = f'{path}/{view_name}.pdf'
        view_img_response = self.conn.query_view_pdf(view_id, parameter_dict=encoded_filters)
        with open(download_path , 'wb') as file:
            file.write(view_img_response.content)
        print(f'Image saved: {download_path}')
