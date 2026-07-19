import pandas as pd
from src.finance_dashboard.classifier import classify_transactions

def test_classifier_matches_keyword():
    df = pd.DataFrame({
        "description": ["Roman Bauer", "Unknown Shop"],
        "amount": [-450, -10]
    })
    rules = pd.DataFrame({
        "keyword": ["Roman Bauer"],
        "category": ["Rent"],
        "group": ["Needs"],
        "ignore": [False],
        "confidence": ["high"]
    })

    out = classify_transactions(df, rules, "Unclassified", "Review")
    assert out.loc[0, "category"] == "Rent"
    assert out.loc[1, "category"] == "Unclassified"
