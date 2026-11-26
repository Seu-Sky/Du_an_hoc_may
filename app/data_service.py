import pandas as pd
from .config import DATA_PATH

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError("Chưa có dữ liệu. Hãy tải file CSV lên trước.")
    return pd.read_csv(DATA_PATH)

def clean_data(df):
    before_rows, before_cols = len(df), len(df.columns)
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    duplicate_rows = int(out.duplicated().sum())
    out = out.drop_duplicates()
    for col in out.select_dtypes(include=["object"]).columns:
        out[col] = out[col].map(lambda v: v.strip() if isinstance(v, str) else v)
    missing_before = int(out.isna().sum().sum())
    if "Attrition" in out.columns:
        out = out.dropna(subset=["Attrition"])
    for col in out.columns:
        if out[col].isna().any():
            if pd.api.types.is_numeric_dtype(out[col]):
                out[col] = out[col].fillna(out[col].median())
            else:
                mode = out[col].mode(dropna=True)
                out[col] = out[col].fillna(mode.iloc[0] if len(mode) else "Unknown")
    log = {"rows_before": before_rows, "rows_after": len(out),
           "columns_before": before_cols, "duplicate_rows_removed": duplicate_rows,
           "missing_values_before": missing_before,
           "missing_values_after": int(out.isna().sum().sum())}
    return out, log

def validate_dataset(df):
    if "Attrition" not in df.columns:
        raise ValueError("Không tìm thấy cột Attrition.")
    vals = set(df["Attrition"].dropna().astype(str).str.strip().str.title().unique())
    if not vals.issubset({"Yes", "No"}):
        raise ValueError("Attrition phải chứa Yes/No.")
