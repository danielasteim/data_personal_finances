"""
This code is the parsing part of pdf extraction module.
"""
import sys
import pdfplumber
import os   
import pandas as pd

# OPEN PDF FILES WITH POSSIBLE PASSWORDS
def open_pdf(file_path):
    POSSIBLE_PASSWORDS = [
        None,
        "11659"
    ]
    for pwd in POSSIBLE_PASSWORDS:
        try:
            return pdfplumber.open(file_path, password=pwd)
        except:
            continue
    raise ValueError(f"Could not open {file_path}")

# EXTRACT CONTENT TABLES FROM PDF
def extract_tables_from_pdf(file_path):
    tables = []

    with open_pdf(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_tables = page.extract_tables()

            if not page_tables:
                continue

            for table in page_tables:
                # row
                for row in table:
                    # line
                    line = " ".join(cell for cell in row if cell)

                    if line and line[0].isdigit():
                        tables.append(line)
    
    return tables

# GET BANK NAME FROM FILE NAME
def bank_name(file_name):

    bank_keywords = {
        "nubank": "Nubank",
        "inter": "Banco Inter",
        "c6": "C6 Bank",
        "itau": "Itaú",
        "bradesco": "Bradesco",
        "santander": "Santander",
        "bb": "Banco do Brasil",
        "caixa": "Caixa Econômica",
        "sicredi": "Sicredi",
        "xp": "XP Investimentos"
    }

    file_name_lower = file_name.lower()
    for keyword, bank in bank_keywords.items():
        if keyword in file_name_lower:
            return bank
    return "Unknown"

sys.path.append("src")
from cleaner import clean_line

def clean_pdf(file_path):
    raw_lines = extract_tables_from_pdf(file_path)
    cleaned = []

    for line in raw_lines:
        result = clean_line(line)
        if result:
            cleaned.append(result)

    return cleaned


if __name__ == "__main__":
    test_file = "data/raw/Nubank_2025-12-04.pdf"
    data = clean_pdf(test_file)

    for d in data:
        print(d)
