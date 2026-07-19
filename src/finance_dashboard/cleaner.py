import pandas as pd

def find_column(columns, keywords, fallback_index=None):
    lower_map = {str(c).lower(): c for c in columns}
    for key, original in lower_map.items():
        if any(k in key for k in keywords):
            return original
    if fallback_index is not None:
        return columns[fallback_index]
    raise ValueError(f"Could not find column matching {keywords}")

def clean_transactions(raw: pd.DataFrame) -> pd.DataFrame:
    date_col = find_column(raw.columns, ["date"], 0)
    amount_col = find_column(raw.columns, ["amount"], len(raw.columns) - 1)
    desc_col = find_column(
        raw.columns,
        ["description", "merchant", "reference", "details", "counterparty"],
        1
    )

    df = raw.copy()
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["description"] = df[desc_col].astype(str).fillna("")
    df["amount"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0.0)
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df["year"] = df["date"].dt.year
    df["transaction_id"] = (
        df["date"].astype(str) + "|" +
        df["description"].astype(str) + "|" +
        df["amount"].astype(str)
    )

    currency_col = None
    for col in raw.columns:
        if "currency" in str(col).lower():
            currency_col = col
            break
    df["currency"] = raw[currency_col] if currency_col else "EUR"

    return df[[
        "transaction_id",
        "date",
        "month",
        "year",
        "description",
        "amount",
        "currency",
        "source_file"
    ]].drop_duplicates(subset=["transaction_id"])
