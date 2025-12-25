"""
This code is the ingestion part of mail processing. It contains the functions 
to connect to the gmail API, search for emails, and download attachments.
"""

import base64
import os
import pickle 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
email = 'danieladesa01@gmail.com'
ATTACHMENTS_DIR = 'data/raw'

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

# SEARCH FOR EMAILS THAT ARE MAKERD AS UNREAD, RELATED TO THE CREDIT CARD STATEMENT, AND CONTAINS ATTACHMENTS
def search_unread_invoices(service):
    query ='is:unread has:attachment subject:Fatura'
    results = service.users().messages().list(userId='me', q=query).execute()
    return results.get('messages', [])

# DOWNLOAD ATTACHMENTS FROM THE SELECTED EMAILS
# must deal with attachments containing passwords
def download_attachments(service, message_id):
    message = service.users().messages().get(
        userId='me',
        id=message_id
    ).execute()
    file_names = []

    for part in message['payload'].get('parts', []):
        if part.get('filename') and part['filename'].lower().endswith('.pdf'):
            attachment_id = part['body'].get('attachmentId')

            attachment = service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(attachment['data'])
            file_path = os.path.join(ATTACHMENTS_DIR, part['filename'])
            file_names.append(part['filename'])

            with open(file_path, 'wb') as f:
                f.write(file_data)

            print(f"📄 Saved: {file_path}")
            
    return file_names

# MARK EMAILS AS READ AFTER PROCESSING
def mark_as_read(service, message_id):
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

if __name__ == "__main__":
    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

    service = gmail_connection()
    messages = search_unread_invoices(service)

    print(f" Found {len(messages)} unread invoice emails")

    for msg in messages:
        download_attachments(service, msg['id'])
        mark_as_read(service, msg['id'])

    print("Ingestion finished")
