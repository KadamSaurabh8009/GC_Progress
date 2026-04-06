from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io

from app.schemas.request import RecipeQueryRequest
from app.schemas.response import RecipeQueryResponse
from app.services.query_service import QueryService
from app.services.vision_service import VisionService  # ✅ correct


router = APIRouter()

query_service = QueryService(top_k=3)
vision_service = VisionService()  # ✅ fixed


@router.post("/query", response_model=RecipeQueryResponse)
def query_recipes(request: RecipeQueryRequest):
    answer = query_service.process_query(
        query=request.query,
        cuisine=request.cuisine,
        max_time=request.max_time,
        veg_only=request.veg_only
    )
    return RecipeQueryResponse(answer=answer)


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/vision")
async def describe_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    description = vision_service.describe_image(image)

    return {
        "description": description
    }