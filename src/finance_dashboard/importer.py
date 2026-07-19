from pathlib import Path
import pandas as pd

def read_statement(csv_path: Path) -> pd.DataFrame:
    """Read a bank CSV using a flexible separator strategy."""
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(csv_path, sep=sep)
            if df.shape[1] >= 3:
                return df
        except Exception:
            continue
    return pd.read_csv(csv_path)

def read_all_statements(statements_dir: Path) -> pd.DataFrame:
    files = sorted(statements_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {statements_dir}")

    frames = []
    for file in files:
        df = read_statement(file)
        df["source_file"] = file.name
        frames.append(df)

    return pd.concat(frames, ignore_index=True)
