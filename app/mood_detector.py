# app/mood_detector.py

import torch
import clip
from PIL import Image

# Device setup: GPU if available, otherwise CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Define the list of moods your app can detect
mood_options = [
    "Calm", "Energetic", "Happy", "Sad", "Nostalgic",
    "Dark", "Romantic", "Excited","Chill"
       
 

]

def detect_mood(image_path):
    """
    Returns the mood that best matches the uploaded photo.
    """
    # Load and preprocess the image
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Prepare text descriptions for moods
    text = clip.tokenize(mood_options).to(device)
    
    # Compute similarity between image and text
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
        # Normalize features
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
        # Compute cosine similarity
        similarity = (100.0 * image_features @ text_features.T)
        values, indices = similarity[0].topk(1)
        
        # Return the mood with highest similarity
        return mood_options[indices[0]]
