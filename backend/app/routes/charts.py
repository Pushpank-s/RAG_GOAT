from fastapi import APIRouter, UploadFile, File, Form

from app.services.csv_loader import load_file
from app.services.feature_extractor import extract_features
from app.services.chart_generator import generate_chart

router = APIRouter(
    prefix="/charts",
    tags=["Charts"]
)


@router.post("/generate")
async def generate_chart_api(
    file: UploadFile = File(...),
    chart_type: str = Form(...)
):
    df = load_file(file)

    metadata = extract_features(df)

    x = metadata["recommended_x"]
    y = metadata["recommended_y"]

    chart_json = generate_chart(
        df=df,
        chart_type=chart_type,
        x=x,
        y=y
    )

    return {
        "chart_type": chart_type,
        "x_axis": x,
        "y_axis": y,
        "chart": chart_json
    }