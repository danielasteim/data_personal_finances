import pdfplumber
import re
import pandas as pd
import os


RAW_DATA = "data/raw"
READ_FILES_PATH = "data/processed/read_files.txt"

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
            
            if "Data Descrição R$" not in text:
                continue
           
            lines = text.split('\n')
            table_section = False
            table_lines = []
            
            for line in lines:  
                if re.search(r"Data\s+Descrição\s+R\$", line):
                    table_section = True
                if re.search(r"Subtotal|Total|Resumo", line):
                    table_section = False
                    continue
                if table_section:
                    table_lines.append(line)
                    continue
            
            # Regex: Data, Descrição Valor
            pattern = r"(\d{2}/\d{2}/\d{2})\s+(.+?)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+0,00"
            for line in table_lines:
                data = re.match(pattern, line.strip())
                if data:
                    date, desc, value = data.groups()
                    value = float(value.replace(".", "").replace(",", "."))
                    transactions.append([date, desc.strip(), value])
            

    # Cria DataFrame
    df = pd.DataFrame(transactions, columns=["Data", "Descrição", "Valor (R$)"])
    return df


if __name__ == "__main__":
    
    # Create output folder for CSV files
    OUTPUT_DIR = "data/processed"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # GET A STRING LIST ALL FILES OF RAW DATA 
    all_files = [os.path.join(RAW_DATA, f) for f in os.listdir(RAW_DATA) if f.endswith('.pdf')]
    all_dataframes = []

    # READS ALL ALREADY PROCESSED FILES FORM TXT FILE
    if os.path.exists(READ_FILES_PATH):
        with open(READ_FILES_PATH, "r") as f:
            read_files = [line.strip() for line in f.readlines()]
    else:
        read_files = []
        
    with open("ps.txt", "r") as f:
        passw = f.read().strip()
        
    for pdf_file in all_files:
        if pdf_file in read_files:
            continue
        else:
            print(f"Processing file: {pdf_file}")
            try:
                df = extract_transactions(pdf_file, passw)
                print(df)
                
                # Get filename without extension
                base_name = os.path.splitext(os.path.basename(pdf_file))[0]
                csv_filename = base_name + '.csv'
                csv_path = os.path.join(OUTPUT_DIR, csv_filename)
                df.to_csv(csv_path, index=False, encoding='utf-8')
                print(f"Saved CSV file: {csv_filename}")
                
                all_dataframes.append(df)
                read_files.append(pdf_file)
                with open(READ_FILES_PATH, "a") as f:
                    f.write(pdf_file + "\n")
                    
            except Exception as e:
                print(f"Error: {pdf_file}: {str(e)}")