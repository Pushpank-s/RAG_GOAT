from fastapi import APIRouter, UploadFile, File

from app.services.csv_loader import load_file
from app.services.feature_extractor import extract_features
from app.services.recommendation_engine import recommend_charts

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendation"]
)


@router.post("/")
async def recommend(file: UploadFile = File(...)):

    df = load_file(file)

    metadata = extract_features(df)

    recommendations = recommend_charts(metadata)

    return {
        "metadata": metadata,
        "recommendations": recommendations
    }