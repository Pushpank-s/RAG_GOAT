from fastapi import APIRouter, UploadFile, File

from app.services.csv_loader import load_file
from app.services.feature_extractor import extract_features

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_csv(file: UploadFile = File(...)):

    df = load_file(file)

    metadata = extract_features(df)

    return {

        "metadata": metadata,

        "preview": df.head().to_dict(
            orient="records"
        )
    }