"""
Streamlit UI for reviewing unclassified transactions and feeding new rules
back into the classification system.

Run from project root:

    streamlit run ui/review_unclassified.py
"""

from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.finance_dashboard.config import load_settings
from src.finance_dashboard.importer import read_all_statements
from src.finance_dashboard.cleaner import clean_transactions
from src.finance_dashboard.classifier import load_rules, classify_transactions

st.set_page_config(
    page_title="Transaction Categorizer",
    page_icon="💶",
    layout="wide"
)

st.title("💶 Unclassified Transaction Categorizer")
st.caption("Review transactions once, save rules, and future statements will classify automatically.")

settings = load_settings()
statements_dir = ROOT_DIR / settings["paths"]["statements_dir"]
rules_file = ROOT_DIR / settings["paths"]["rules_file"]

def load_current_data():
    raw = read_all_statements(statements_dir)
    cleaned = clean_transactions(raw)
    rules = load_rules(rules_file)
    classified = classify_transactions(
        cleaned,
        rules,
        default_category=settings["classification"]["default_category"],
        default_group=settings["classification"]["default_group"],
    )
    return classified, rules

def save_rule(keyword, category, group, ignore, confidence):
    rules = pd.read_csv(rules_file)
    new_rule = pd.DataFrame([{
        "keyword": keyword.strip(),
        "category": category.strip(),
        "group": group.strip(),
        "ignore": str(bool(ignore)).lower(),
        "confidence": confidence
    }])

    # Avoid exact duplicate keywords
    existing = rules["keyword"].astype(str).str.lower().str.strip()
    if keyword.lower().strip() in set(existing):
        st.warning(f"Rule already exists for keyword: {keyword}")
        return False

    updated = pd.concat([rules, new_rule], ignore_index=True)
    updated.to_csv(rules_file, index=False)
    return True

classified, rules = load_current_data()

usable = classified[classified["ignore"] == False].copy()
unclassified = usable[usable["category"] == settings["classification"]["default_category"]].copy()

st.sidebar.header("Current status")
st.sidebar.metric("Transactions", len(usable))
st.sidebar.metric("Unclassified", len(unclassified))
st.sidebar.metric("Rules", len(rules))

st.sidebar.divider()
st.sidebar.write("Rules file:")
st.sidebar.code(str(rules_file.relative_to(ROOT_DIR)))

existing_categories = sorted(set(rules["category"].dropna().astype(str))) + ["New category"]
existing_groups = sorted(set(rules["group"].dropna().astype(str))) + ["New group"]

tab1, tab2, tab3 = st.tabs(["Review Unclassified", "Rules", "All Transactions"])

with tab1:
    st.subheader("Unclassified transactions")

    if unclassified.empty:
        st.success("No unclassified transactions found. Your rules covered everything.")
    else:
        st.info("Choose a transaction, create a keyword rule, and save it for future imports.")

        display_cols = ["date", "description", "amount", "currency", "source_file"]
        st.dataframe(
            unclassified[display_cols].sort_values("date"),
            use_container_width=True,
            hide_index=True
        )

        descriptions = unclassified["description"].dropna().astype(str).unique().tolist()
        selected_description = st.selectbox("Select transaction description", descriptions)

        selected_rows = unclassified[unclassified["description"] == selected_description]
        st.write("Matching transactions:")
        st.dataframe(
            selected_rows[display_cols],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.subheader("Create classification rule")

        col1, col2 = st.columns(2)

        with col1:
            keyword = st.text_input(
                "Keyword to match in future",
                value=selected_description[:60],
                help="Use the shortest stable part of the description. Example: Roman Bauer, REWE, LemFi."
            )

            category_choice = st.selectbox("Category", existing_categories)
            if category_choice == "New category":
                category = st.text_input("New category name")
            else:
                category = category_choice

        with col2:
            group_choice = st.selectbox("Group", existing_groups)
            if group_choice == "New group":
                group = st.text_input("New group name")
            else:
                group = group_choice

            confidence = st.selectbox("Confidence", ["high", "medium", "low"], index=1)
            ignore = st.checkbox("Ignore this transaction type", value=False)

        if st.button("Save rule", type="primary"):
            if not keyword or not category or not group:
                st.error("Keyword, category, and group are required.")
            else:
                ok = save_rule(keyword, category, group, ignore, confidence)
                if ok:
                    st.success("Rule saved. Re-run the main pipeline to regenerate reports.")
                    st.code("python -m src.finance_dashboard.main")

with tab2:
    st.subheader("Classification rules")
    rules_editor = st.data_editor(
        rules,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True
    )

    if st.button("Save edited rules"):
        rules_editor.to_csv(rules_file, index=False)
        st.success("Rules updated.")

with tab3:
    st.subheader("All classified transactions")
    st.dataframe(
        classified.sort_values("date"),
        use_container_width=True,
        hide_index=True
    )
