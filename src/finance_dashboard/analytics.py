import pandas as pd

def usable_transactions(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["ignore"] == False].copy()

def build_dashboard_metrics(df: pd.DataFrame, small_purchase_threshold: float = 20.0) -> pd.DataFrame:
    usable = usable_transactions(df)
    income = usable.loc[usable["amount"] > 0, "amount"].sum()
    expenses = -usable.loc[usable["amount"] < 0, "amount"].sum()
    small_purchases = usable[(usable["amount"] < 0) & (usable["amount"].abs() < small_purchase_threshold)]

    metrics = [
        ("Total income", income),
        ("Total expenses", expenses),
        ("Net cash flow", income - expenses),
        ("Savings rate", (income - expenses) / income if income else 0),
        ("Transaction count", len(usable)),
        ("Unclassified transactions", int((usable["category"] == "Unclassified").sum())),
        (f"Small purchases under {small_purchase_threshold}", -small_purchases["amount"].sum()),
    ]

    return pd.DataFrame(metrics, columns=["metric", "value"])

def monthly_cash_flow(df: pd.DataFrame) -> pd.DataFrame:
    usable = usable_transactions(df)
    result = usable.groupby("month").agg(
        income=("amount", lambda s: s[s > 0].sum()),
        expenses=("amount", lambda s: -s[s < 0].sum()),
        net_cash_flow=("amount", "sum"),
        transactions=("amount", "count"),
    ).reset_index()
    result["savings_rate"] = result.apply(
        lambda r: r["net_cash_flow"] / r["income"] if r["income"] else 0,
        axis=1
    )
    return result

def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    usable = usable_transactions(df)
    return usable.groupby(["group", "category"]).agg(
        transaction_count=("amount", "count"),
        total_amount=("amount", "sum"),
        absolute_spend=("amount", lambda s: s[s < 0].abs().sum()),
    ).reset_index().sort_values("absolute_spend", ascending=False)

def money_leak_report(df: pd.DataFrame, small_purchase_threshold: float = 20.0, top_n: int = 50) -> pd.DataFrame:
    usable = usable_transactions(df)
    expenses = usable[usable["amount"] < 0].copy()
    small = expenses[expenses["amount"].abs() < small_purchase_threshold].copy()
    small["absolute_amount"] = small["amount"].abs()
    return small.sort_values("absolute_amount", ascending=False).head(top_n)

def top_transactions(df: pd.DataFrame, limit: int = 30) -> pd.DataFrame:
    usable = usable_transactions(df).copy()
    usable["absolute_amount"] = usable["amount"].abs()
    return usable.sort_values("absolute_amount", ascending=False).head(limit)

def unclassified_transactions(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["ignore"] == False) & (df["category"] == "Unclassified")].copy()
