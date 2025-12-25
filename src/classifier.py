# CATEGORIES
CATEGORIES = {
    "TRANSPORT": [
        "PLANE",
        "UBER",
        "TAXI",
        "GAS",
        "BUS",
        "TRAIN",
        "SUBWAY",
        "PARKING",
        "TOLLS"
    ],

    "FOOD": [
        "GROCERIES",
        "OUTINGS",
        "SNACKS",
        "DRINKS",
        "DELIVERY",
        "RESTAURANT"
    ],

    "SHOPPING": [
        "BASICS",
        "GIFTS",
        "CLOTHING",
        "BEAUTY",
        "FACE",
        "ELECTRONICS",
        "OTHER"
    ],

    "HEALTH": [
        "GYM",
        "SPORTS",
        "MEDICAL",
        "PHARMACY",
        "SUPPLEMENTS"
    ],

    "EXPENSES": [
        "HOUSING",
        "ENTERTAINMENT",
        "TRAVEL",
        "EDUCATION",
        "HEALTH",
        "SUBSCRIPTIONS",
        "PHONE"
    ],


    "INCOME": [
        "SALARY",
        "FREELANCE",
        "REFUND",
        "CASHBACK"
    ],

    "OTHER": [
        "DONATIONS",
        "UNKNOWN",
        "UNEXPECTED",
        "MISC"
    ]
}



# LOAD MODEL

# CLASSIFICATION FUNCTION

# TRAINING FUNCTION

# SEE IF MODEL NEEDS RETRAINING
import pandas as pd
from db import connect_to_db

def export_transactions_to_excel(path="transactions_to_classify.xlsx"):
    query = """
        SELECT id, day, month, merchant, amount
        FROM transactions
        ORDER BY id
    """

    conn = connect_to_db()
    df = pd.read_sql(query, conn)
    conn.close()

    df["category"] = ""
    df["subcategory"] = ""

    df.to_csv(path, index=False)
    print(f"Arquivo gerado: {path}")

if __name__ == "__main__":
    export_transactions_to_excel()