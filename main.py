import pdfplumber
import re
import pandas as pd

FILEPATH = "data/raw/Fatura2025-10-05.pdf"

def extract_transactions(filepath, pw=None, start_page=2):
    transactions = []

    with pdfplumber.open(filepath, password=pw) as pdf:
        # Itera pelas páginas a partir da 3ª (índice 2)
        for page_num in range(start_page, len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
            

            # print(text)
            
            if "Data Descrição R$" in text:
                table_text = text.split("Data Descrição R$")[-1]
            else:
                continue

            table_text = re.split(r"Subtotal|Total|Resumo", table_text)[0]

            # Regex: Data, Descrição Valor
            pattern = r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+0,00"
            matches = re.findall(pattern, table_text)

            for date, desc, value in matches:
                value = float(value.replace(".", "").replace(",", "."))
                transactions.append([date, desc.strip(), value])

    # Cria DataFrame
    df = pd.DataFrame(transactions, columns=["Data", "Descrição", "Valor (R$)"])
    return df


if __name__ == "__main__":
    df = extract_transactions(FILEPATH, pw="11659")
    print(df)
    print(f"\n{len(df)} transações encontradas.")
