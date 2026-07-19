# Feedback Loop Architecture

## Purpose

The categorizer UI turns human corrections into reusable classification rules.

## Flow

```text
Bank CSV
  ↓
Cleaner
  ↓
Classifier
  ↓
Unclassified Transactions
  ↓
Review UI
  ↓
classification_rules.csv
  ↓
Future classification
```

## Why this matters

Bank descriptions are often unclear. Instead of hardcoding everything in Python,
the system lets the user teach the classifier over time.

## Current approach

Rule-based matching:

```text
if keyword appears in description:
    assign category/group/ignore flag
```

## Future upgrades

- Suggest category using previous similar transactions
- Use fuzzy matching
- Train a local machine learning classifier
- Add approval queue
- Add merchant normalization
- Store rules in SQLite instead of CSV
- Web dashboard with Vaadin or FastAPI
