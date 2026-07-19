from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def _save_chart(fig, output_path: Path) -> str:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return str(output_path)

def chart_monthly_cash_flow(monthly: pd.DataFrame, charts_dir: Path) -> str:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly["month"], monthly["income"], marker="o", label="Income")
    ax.plot(monthly["month"], monthly["expenses"], marker="o", label="Expenses")
    ax.plot(monthly["month"], monthly["net_cash_flow"], marker="o", label="Net cash flow")
    ax.set_title("Monthly Cash Flow")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.25)
    return _save_chart(fig, charts_dir / "monthly_cash_flow.png")

def chart_category_spending(categories: pd.DataFrame, charts_dir: Path, top_n: int = 10) -> str:
    data = categories.sort_values("absolute_spend", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(data["category"], data["absolute_spend"])
    ax.set_title(f"Top {top_n} Spending Categories")
    ax.set_xlabel("Spend")
    ax.set_ylabel("Category")
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.25)
    return _save_chart(fig, charts_dir / "top_spending_categories.png")

def chart_group_spending(categories: pd.DataFrame, charts_dir: Path) -> str:
    data = categories.groupby("group", as_index=False)["absolute_spend"].sum()
    data = data[data["absolute_spend"] > 0].sort_values("absolute_spend", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    if data.empty:
        ax.text(0.5, 0.5, "No spending data", ha="center", va="center")
        ax.axis("off")
    else:
        ax.pie(data["absolute_spend"], labels=data["group"], autopct="%1.1f%%", startangle=90)
        ax.set_title("Spending by Group")
    return _save_chart(fig, charts_dir / "spending_by_group.png")

def chart_money_leaks(leaks: pd.DataFrame, charts_dir: Path, top_n: int = 15) -> str:
    if leaks.empty:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No small-purchase leaks found", ha="center", va="center")
        ax.axis("off")
        return _save_chart(fig, charts_dir / "money_leaks.png")

    data = leaks.copy()
    data["label"] = data["description"].astype(str).str[:28]
    data = data.sort_values("absolute_amount", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(data["label"], data["absolute_amount"])
    ax.set_title(f"Top {top_n} Small Purchases / Money Leaks")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Transaction")
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.25)
    return _save_chart(fig, charts_dir / "money_leaks.png")

def generate_charts(monthly: pd.DataFrame, categories: pd.DataFrame, leaks: pd.DataFrame, charts_dir: Path) -> dict:
    charts_dir.mkdir(parents=True, exist_ok=True)
    return {
        "monthly_cash_flow": chart_monthly_cash_flow(monthly, charts_dir),
        "top_spending_categories": chart_category_spending(categories, charts_dir),
        "spending_by_group": chart_group_spending(categories, charts_dir),
        "money_leaks": chart_money_leaks(leaks, charts_dir),
    }
