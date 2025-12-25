import cleaner as clean
import mail
import pdfparser as pdf
import db


def process_file(file_name):
    existing = db.file_exists(file_name)

    if existing:
        file_id, processed = existing
        if processed:
            print(f"Skipping already processed file: {file_name}")
            return
        else:
            print(f"Resuming unprocessed file: {file_name}")
    else:
        file_id = db.insert_file(
            file_name,
            bank=pdf.bank_name(file_name)
        )

    try:
        transactions = pdf.clean_pdf(f"data/raw/{file_name}")
        db.insert_transactions(file_id, transactions)
        db.mark_file_processed(file_id)
        print(f"Processed file: {file_name}")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        raise

def main():
    service = mail.gmail_connection()
    messages = mail.search_unread_invoices(service)

    print(f"Found {len(messages)} unread invoice emails")

    for msg in messages:
        files = mail.download_attachments(service, msg["id"])

        for file_name in files:
            process_file(file_name)

        mail.mark_as_read(service, msg["id"])

    print("Ingestion finished")


if __name__ == "__main__":
    main()
