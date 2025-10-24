from pydantic import BaseModel, Field
from typing import Optional

class StagingRequest(BaseModel):
    """
    Pydantic model for user-provided prompts.
    Users can override the default prompts to tune the scoring logic.
    """
    prompt_good: str = Field(
        "an empty room ideal for virtual staging: large visible floor space, clear walls and corners, windows visible and not blocked, no doorway in the middle, evenly lit with natural light, aesthetically pleasing",
        description="A descriptive prompt for what makes a room suitable for staging."
    )
    prompt_bad: str = Field(
        "a room that is hard to stage: narrow, cluttered, windows blocked, poor lighting, doorway or obstacles in the center, little open space",
        description="A descriptive prompt for what makes a room unsuitable for staging."
    )
    prompt_aesthetic: Optional[str] = Field(
        None,
        description="An optional plus-prompt for aesthetic qualities like 'modern fireplace' or 'hardwood floors'."
    )

class StagingResponse(BaseModel):
    """
    Pydantic model for the API response.
    """
    filename: str
    stageability_score: float = Field(..., description="The calculated differential score (good - bad).")
    details: str