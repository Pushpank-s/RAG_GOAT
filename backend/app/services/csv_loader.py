import pandas as pd


def load_file(file):
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file.file)

    elif filename.endswith(".xlsx"):
        return pd.read_excel(file.file)

    else:
        raise ValueError("Unsupported file type")