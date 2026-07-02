import pandas as pd


def detect_datetime_columns(df):


    datetime_cols = []

    for col in df.columns:

        if df[col].dtype != "object":
            continue

        try:
            converted = pd.to_datetime(df[col], errors="coerce")

            success_rate = converted.notna().mean()

            if success_rate >= 0.8:
                datetime_cols.append(col)

        except Exception:
            pass

    return datetime_cols

def convert_numeric_columns(df):


    for col in df.columns:

        if df[col].dtype == "object":

            converted = pd.to_numeric(df[col], errors="coerce")

            success_rate = converted.notna().mean()

            if success_rate >= 0.8:
                df[col] = converted

    return df


def extract_features(df):
    df = convert_numeric_columns(df)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    datetime_cols = detect_datetime_columns(df)

    missing_ratio = (
        df.isnull().sum().sum()
        /
        (len(df) * len(df.columns))
    )

    duplicate_rows = int(df.duplicated().sum())

    avg_cardinality = float(df.nunique().mean())

    numeric_df = df.select_dtypes(include="number")

    if len(numeric_df.columns) > 1:
        correlation = float(
            numeric_df.corr().abs().mean().mean()
        )
    else:
        correlation = 0

    recommended_x = None
    recommended_y = None

    # Prefer time-series
    if datetime_cols and numeric_cols:
        recommended_x = datetime_cols[0]
        recommended_y = numeric_cols[0]

    # Compare categories
    elif categorical_cols and numeric_cols:
        recommended_x = categorical_cols[0]

        preferred_numeric = [
            col for col in numeric_cols
            if "id" not in col.lower()
        ]

        recommended_y = (
            preferred_numeric[0]
            if preferred_numeric
            else numeric_cols[0]
        )

    # Relationship
    elif len(numeric_cols) >= 2:

        preferred_numeric = [
            col for col in numeric_cols
            if "id" not in col.lower()
        ]

        if len(preferred_numeric) >= 2:
            recommended_x = preferred_numeric[0]
            recommended_y = preferred_numeric[1]
        else:
            recommended_x = numeric_cols[0]
            recommended_y = numeric_cols[1]

    column_cardinality = {}

    for col in df.columns:
        column_cardinality[col] = int(df[col].nunique())
    return {

        "rows": len(df),

        "columns": len(df.columns),

        "numeric_columns": len(numeric_cols),

        "categorical_columns": len(categorical_cols),

        "datetime_columns": len(datetime_cols),

        "numeric_column_names": numeric_cols,

        "categorical_column_names": categorical_cols,

        "datetime_column_names": datetime_cols,

        "missing_ratio": round(missing_ratio, 3),

        "duplicate_rows": duplicate_rows,

        "avg_cardinality": round(avg_cardinality, 2),

        "correlation": round(correlation, 2),

        "column_cardinality": column_cardinality,

        "recommended_x": recommended_x,

        "recommended_y": recommended_y
    }