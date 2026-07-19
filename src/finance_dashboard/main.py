from pathlib import Path

from .config import ROOT_DIR, load_settings
from .importer import read_all_statements
from .cleaner import clean_transactions
from .classifier import load_rules, classify_transactions
from .database import save_transactions
from .reports import export_reports

def main():
    settings = load_settings()

    statements_dir = ROOT_DIR / settings["paths"]["statements_dir"]
    rules_file = ROOT_DIR / settings["paths"]["rules_file"]
    db_file = ROOT_DIR / settings["paths"]["database_file"]

    raw = read_all_statements(statements_dir)
    cleaned = clean_transactions(raw)

    rules = load_rules(rules_file)
    classified = classify_transactions(
        cleaned,
        rules,
        default_category=settings["classification"]["default_category"],
        default_group=settings["classification"]["default_group"],
    )

    save_transactions(db_file, classified)
    outputs = export_reports(classified, settings)

    print("Finance dashboard generated successfully.")
    print(f"Excel report: {outputs['excel']}")
    print(f"CSV summary: {outputs['csv']}")
    print(f"Reports folder: {outputs['reports_dir']}")

if __name__ == "__main__":
    main()
