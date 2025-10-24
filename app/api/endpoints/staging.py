from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from PIL import Image
import io
from app.models.clip_model import staging_ranker
from app.schemas.staging import StagingRequest, StagingResponse

router = APIRouter()

@router.post("/rank_image", response_model=StagingResponse)
async def rank_image_for_staging(
    prompts: StagingRequest = Depends(),
    file: UploadFile = File(...)
):
    """
    Accepts an image upload and optional JSON prompts to compute a stageability score.
    
    - **file**: The image file to be analyzed.
    - **prompts**: A JSON object with `prompt_good`, `prompt_bad`, and optional `prompt_aesthetic`.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=500, detail="Could not process the uploaded image.")

    score = staging_ranker.compute_score(image, prompts)
    
    return StagingResponse(
        filename=file.filename,
        stageability_score=score,
        details="Score calculated based on the provided prompts."
    )