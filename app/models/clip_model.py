import torch
import open_clip
from PIL import Image
from mobileclip.modules.common.mobileone import reparameterize_model
from app.core.config import settings
from app.schemas.staging import StagingRequest

class StagingRanker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StagingRanker, cls).__new__(cls)
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        """
        Loads the MobileCLIP2 model and tokenizer into memory.
        This is a time-consuming operation and should only be done once.
        """
        print("Loading MobileCLIP2 model...")
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            settings.MODEL_NAME, 
            pretrained=settings.MODEL_PATH
        )
        self.tokenizer = open_clip.get_tokenizer(settings.MODEL_NAME)
        self.model.eval()
        self.model = reparameterize_model(self.model)
        print("Model loaded successfully.")

    def compute_score(self, image: Image.Image, prompts: StagingRequest) -> float:
        """
        Computes the differential stageability score for a given image and prompts.
        """
        image_tensor = self.preprocess(image.convert("RGB")).unsqueeze(0)
        
        text_prompts = [prompts.prompt_good, prompts.prompt_bad]
        if prompts.prompt_aesthetic:
            text_prompts.append(prompts.prompt_aesthetic)
            
        text_tokens = self.tokenizer(text_prompts)

        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)
            text_features = self.model.encode_text(text_tokens)

            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            sims = (image_features @ text_features.T)[0]
            
            score = (sims[0] - sims[1]).item()
            
            if prompts.prompt_aesthetic:
                score += sims[2].item()
                
            return score

staging_ranker = StagingRanker()