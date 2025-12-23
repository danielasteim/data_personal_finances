"""
This code is the ingestion part of mail processing. It contains the functions 
to connect to the gmail API, search for emails, and download attachments.
"""

import os
import pickle 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
email = 'danieladesa01@gmail.com'

# CONNECT TO GMAIL API
def gmail_connection():
    session_credentials = None

    # Uses picle and os to save the token for future use
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            session_credentials = pickle.load(token)

    # login to gmail API using the downloaded json credentials
    if not session_credentials or not session_credentials.valid:
        if session_credentials and session_credentials.expired and session_credentials.refresh_token:
            session_credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            session_credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(session_credentials, token)
    return build('gmail', 'v1', credentials=session_credentials)


if __name__ == "__main__":
    service = gmail_connection()
    profile = service.users().getProfile(userId='me').execute()
    print("Connected to Gmail API")
    print("Email:", profile['emailAddress'])

# SEARCH FOR EMAILS THAT ARE MAKERD AS UNREAD, RELATED TO THE CREDIT CARD STATEMENT, AND CONTAINS ATTACHMENTS

# DOWNLOAD ATTACHMENTS FROM THE SELECTED EMAILS
# must deal with attachments containing passwords

# MARK EMAILS AS READ AFTER PROCESSING

