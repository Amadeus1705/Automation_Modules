class EmailSender:
    """
    A class to send emails using an SMTP server.

    Attributes:
    - sender_name (str): The name of the sender.
    - sender_email (str): The email address of the sender.
    - sender_passwd (str): The password of the sender's email account.

    Methods:
    - send_email(receiver_email, cc_recipient, subject, body, attachments=None, add_image_as_body=None): Sends an email with the specified details.
        
        Sends an email with the specified details.

        Parameters:
            - receiver_email (str): The email address of the recipient.
            - cc_recipient (Optional[str]): The email address of the CC recipient. Defaults to None.
            - subject (str): The subject of the email.
            - body (str): The body of the email.
            - attachments (Optional[List[str]]): A list of file paths to attach to the email. Defaults to None.
            - add_image_as_body (Optional[List[str]]): A list of image file paths to embed in the email body. Defaults to None.

        Example Usage:
            - sender = EmailSender('Sender Name', 'sender@example.com', 'password')
            - sender.send_email(
                receiver_email='recipient@example.com',
                cc_recipient='cc@example.com',
                subject='Test Email',
                body='This is a test email.',
                attachments=['/path/to/file1.txt', '/path/to/file2.pdf'],
                add_image_as_body=['/path/to/image1.jpg']
            )
    """

    def __init__(self, sender_name: str, sender_email: str, sender_passwd: str):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.sender_passwd = sender_passwd

    def send_email(self, 
                   receiver_email: str, 
                   cc_recipient: Optional[str], 
                   subject: str, 
                   body: str,
                   attachments: Optional[List[str]] = None, 
                   add_image_as_body: Optional[List[str]] = None ):
        
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = receiver_email
        if cc_recipient:
            msg['Cc'] = cc_recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body))


        # Attach body
        if add_image_as_body:
            for filename in add_image_as_body:
                image_name = filename.split('''/''')[-1].split('.')[0]
                text = MIMEText('<img src="cid:image1">', 'html') 
                msg.attach(text)
                image = MIMEImage(open(filename, 'rb').read())
                image.add_header('Content-ID', "<image1>")
                msg.attach(image)
    

        # Attachments
        if attachments:
            for filename in attachments:
                with open(filename, "rb") as attachment:
                    part = MIMEApplication(attachment.read(), Name=filename)
                    part['Content-Disposition'] = f'attachment; filename="{filename.split("/")[-1]}"'
                    msg.attach(part)



        # Connect to the SMTP server
        with smtplib.SMTP('142.250.4.108', 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_passwd)
            server.send_message(msg)
            server.quit()
