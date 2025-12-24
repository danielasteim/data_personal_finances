"""
Dates padronization functions.
Values conversion
Cleaning strings and null values
TRansaction hashing

"""

"""
Generic token-based cleaner for credit card transaction lines.
"""

MONTHS = {
    "JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
    "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"
}


def clean_line(line: str):
    # normalize
    line = line.replace("|", " ").replace("R$", "").strip()
    tokens = line.split()

    day = None
    month = None
    merchant_tokens = []
    amount = None

    for token in tokens:
        # date like 11/11/25
        if "/" in token:
            parts = token.split("/")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                day = parts[0]
                month = parts[1]
                continue

        # textual month (OUT, NOV, ...)
        if token.upper() in MONTHS:
            month = token.upper()
            continue

        # day as number
        if token.isdigit() and len(token) <= 2 and not day:
            day = token
            continue

        # monetary value (3,50 or 11,90)
        if "," in token and token.replace(",", "").replace(".", "").isdigit() and int(token[0]) > 0:
            amount = token
            continue

        # merchant / description
        if token.isalpha() or not any(char.isdigit() for char in token):
            merchant_tokens.append(token)

    if day and month and amount:
        return {
            "day": day,
            "month": month,
            "merchant": " ".join(merchant_tokens).strip(),
            "amount": amount
        }

    return None


