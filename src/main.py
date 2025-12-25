import classifier
import cleaner as clean
import mail 
import pdfparser as pdf
import db

if __name__ == "__main__":
    # SEARCH FOR FILES IN INBOX WITH GMAIL API
    service = mail.gmail_connection()
    messages = mail.search_unread_invoices(service)
    print(f" Found {len(messages)} unread invoice emails")

    # DOWNLOAD FILES AND MARK EMAILS AS READ
    for msg in messages:
        files = mail.download_attachments(service, msg['id'])
        for file_name in files:
            # add file to files table in the database 
            file_id = db.insert_file(file_name, bank=pdf.bank_name(file_name))

            # extract tables from pdf
            transactions = pdf.clean_pdf(f"data/raw/{file_name}")

            # insert transactions into the database
            db.insert_transactions(file_id, transactions)

            # mark file as processed
            db.mark_file_processed(file_id)
            
        mail.mark_as_read(service, msg['id'])

    print("Ingestion finished")
