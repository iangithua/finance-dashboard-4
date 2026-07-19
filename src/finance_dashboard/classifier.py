from pathlib import Path
import pandas as pd

def load_rules(rules_file: Path) -> pd.DataFrame:
    rules = pd.read_csv(rules_file)
    rules["keyword"] = rules["keyword"].astype(str)
    rules["ignore"] = rules["ignore"].astype(str).str.lower().isin(["true", "1", "yes"])
    return rules

def classify_transactions(df: pd.DataFrame, rules: pd.DataFrame, default_category: str, default_group: str) -> pd.DataFrame:
    classified = df.copy()
    classified["category"] = default_category
    classified["group"] = default_group
    classified["ignore"] = False
    classified["confidence"] = "none"
    classified["matched_rule"] = ""

    for _, rule in rules.iterrows():
        keyword = str(rule["keyword"]).lower()
        mask = classified["description"].str.lower().str.contains(keyword, na=False, regex=False)
        unmatched_or_lower_conf = classified["category"].eq(default_category)
        final_mask = mask & unmatched_or_lower_conf

        classified.loc[final_mask, "category"] = rule["category"]
        classified.loc[final_mask, "group"] = rule["group"]
        classified.loc[final_mask, "ignore"] = bool(rule["ignore"])
        classified.loc[final_mask, "confidence"] = rule.get("confidence", "medium")
        classified.loc[final_mask, "matched_rule"] = rule["keyword"]

    classified["flow_type"] = classified["amount"].apply(lambda x: "Income" if x > 0 else "Expense" if x < 0 else "Zero")
    return classified
