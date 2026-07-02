from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        return {"error": "Unsupported file type"}

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "preview": df.head().to_dict(orient="records")
    }