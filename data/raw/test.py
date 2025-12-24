import os
import pdfplumber

nubank_file = 'data/raw/Nubank_2025-12-04.pdf'
xp_file = 'data/raw/9180716-Xp-05-12-2025.pdf'

OUTPUT_DIR = 'data/processed'

POSSIBLE_PASSWORDS = [
    None,
    "11659"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)


def open_pdf(file_path):
    for pwd in POSSIBLE_PASSWORDS:
        try:
            return pdfplumber.open(file_path, password=pwd)
        except:
            continue
    raise ValueError(f"Could not open {file_path}")


def explore_pdf_to_txt(file_path):
    file_name = os.path.basename(file_path).replace('.pdf', '.txt')
    output_path = os.path.join(OUTPUT_DIR, file_name)

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(f"FILE: {file_path}\n")
        out.write("=" * 80 + "\n\n")

        pdf = open_pdf(file_path)

        with pdf:
            for i, page in enumerate(pdf.pages, start=1):
                out.write(f"\n--- PAGE {i} ---\n\n")

                # TEXT
                text = page.extract_text()
                out.write("[TEXT EXTRACT]\n")
                out.write((text or "NO TEXT EXTRACTED") + "\n\n")

                # TABLES
                tables = page.extract_tables()
                out.write(f"[TABLES FOUND]: {len(tables)}\n\n")

                for t_idx, table in enumerate(tables, start=1):
                    out.write(f"Table {t_idx}:\n")
                    for row in table[:50]:
                        out.write(" | ".join(str(cell) for cell in row) + "\n")
                    out.write("\n")

    print(f"Saved exploration to {output_path}")


for file in [nubank_file, xp_file]:
    explore_pdf_to_txt(file)
