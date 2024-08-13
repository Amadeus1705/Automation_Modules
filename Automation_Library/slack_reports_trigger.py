class SlackReportsTrigger:
    """
    A class to trigger notifications and file uploads to Slack.

    Attributes:
    - slack_token (str): The Slack API token used for authentication.

    Methods:
    - send_slack_notification(channel, message, user_mentions=None, title=None): Sends a text notification to a Slack channel.
        Sends a text notification to a Slack channel.
        
        Parameters:
        - channel (str): The name or ID of the Slack channel to send the notification to.
        - message (str): The message content of the notification.
        - user_mentions (List[str], optional): List of user IDs to mention in the notification message. Defaults to None.
        - title (str, optional): The title of the notification message. Defaults to None.

        Returns:
        - None

        Example Usage:
   
    - send_image_as_body(text, file_list=None): Sends a message with embedded images to a Slack channel.
        Sends a message with embedded images to a Slack channel.

          Parameters:
          - text (str): The text content of the message.
          - file_list (List[str], optional): List of file paths of images to embed in the message. Defaults to None.

          Returns:
          - None

          Example Usage:
    
    - send_file_to_slack(channel, file_path, title, user_mentions=None, message=None): Uploads a file to a Slack channel with an optional message.
        Uploads a file to a Slack channel with an optional message.

        Parameters:
        - channel (str): The name or ID of the Slack channel to upload the file to.
        - file_path (str): The path to the file to be uploaded.
        - title (str): The title of the file.
        - user_mentions (List[str], optional): List of user IDs to mention in the message. Defaults to None.
        - message (str, optional): The message content to accompany the file. Defaults to None.

        Returns:
        - None

        Example Usage:
        
    
    
    
    - delete_slack_message(channel_id, timestamp): Deletes a message from a Slack channel using Slack API.

        Deletes a message from a Slack channel using Slack API.

        Parameters:
        - channel_id (str): The ID of the Slack channel containing the message.
        - timestamp (str): The timestamp of the message to be deleted.

        Returns:
        - None

        Example Usage:
        
    """


    def __init__(self, slack_token=None):
        self.slack_token = slack_token 
        

    def send_slack_notification(self, channel, message, user_mentions=None, title=None):
        client = WebClient(token=self.slack_token)
        try:
            mention_text = ' '.join([f'<@{user}>' for user in user_mentions]) if user_mentions else ''
            if title:
                message = f"\n*{title}*\n{message}"
            response = client.chat_postMessage(
                channel=channel,
                text=f"{mention_text} {message}"
            )
            print("Notification sent successfully!")
        except SlackApiError as e:
            print(f"Error sending notification: {e.response['error']}")
        except Exception as e:
            print(f'Encountered Error: {e}')
    

    def send_image_as_body(self, text, file_list=None):
        if file_list != None:
            for file in file_list:
                upload = self.client.files_upload_v2(file=file, filename=file.split('/')[-1])
                text = text + "<" + upload["file"]["permalink"] + "| >"
        self.text = text
        response = self.client.chat_postMessage(channel=self.channel_name, text=text)
        print('Slack message has been sent!')


    def send_file_to_slack(self, channel, file_path, title, user_mentions=None, message=None):
        client = WebClient(token=self.slack_token)
        try:
            mention_text = ' '.join([f'<@{user}>' for user in user_mentions]) if user_mentions else ''
            if message:
                message = f"{message}\n"
                
            file_type, _ = mimetypes.guess_type(file_path)
            
            if file_type == 'text/csv':
                with open(file_path, 'r') as f:
                    csv_content = f.read()
                response = client.files_upload(
                    channels=channel,
                    content=csv_content,
                    title=title,
                    filetype='csv',
                    filename=title,
                    initial_comment=f"{mention_text} {message}" if mention_text or message else None
                )
            elif file_type == 'application/pdf':
                with open(file_path, 'rb') as f:
                    pdf_content = f.read()
                
                response = client.files_upload(
                    channels=channel,
                    content=pdf_content,
                    title=title,
                    filetype=file_type,
                    filename=title,
                    initial_comment=f"{mention_text} {message}" if mention_text or message else None
                )
            elif file_type.startswith('image'):
                with open(file_path, 'rb') as f:
                    image_content = f.read()
                
                response = client.files_upload(
                    channels=channel,
                    content=image_content , 
                    title=title,
                    filetype=file_type,
                    filename=title,
                    initial_comment=f"{mention_text} {message}" if mention_text or message else None
                )
            else:
                print("Unsupported file type")
                return
            print("File uploaded successfully!")
        except SlackApiError as e:
            print(f"Error uploading file: {e.response['error']}")
        except Exception as e:
            print(f'Encountered Error: {e}')
    import requests


    def delete_slack_message(self, channel_id, timestamp):
        # Set up the API endpoint and headers
        url = 'https://slack.com/api/chat.delete'
        headers = {
            'Authorization': f'Bearer {self.slack_token}',
            'Content-Type': 'application/json'
        }

        # Set up the payload with the channel ID and timestamp
        payload = {
            'channel': channel_id,
            'ts': timestamp
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=payload)

        # Check the response
        if response.ok and response.json().get('ok'):
            print('Message deleted successfully')
        else:
            print(f'Failed to delete message: {response.json()}')
