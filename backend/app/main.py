from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.recommend import router as recommend_router
from app.routes.charts import router as chart_router

# Create the FastAPI app FIRST
app = FastAPI(title="ChartSense AI")

# Then configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Then register routes
app.include_router(upload_router)
app.include_router(recommend_router)
app.include_router(chart_router)


@app.get("/")
def root():
    return {
        "message": "ChartSense AI Backend Running "
    }