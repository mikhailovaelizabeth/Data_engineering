def validate_basic(df, required_columns=None, max_rows_in_db=100):
    issues = {}
    if df.empty:
        issues["empty"] = True
    if required_columns:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            issues["missing_columns"] = missing
    issues["rows_total"] = len(df)
    issues["rows_to_db"] = min(len(df), max_rows_in_db)
    return issues
