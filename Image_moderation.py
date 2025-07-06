from torchvision import models, transforms
from PIL import Image
import torch
from transformers import pipeline

model = models.resnet18(pretrained=True)
model.eval()

labels = ['safe', 'nsfw']  # Example labels
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def moderate_image(image_path):
    image = Image.open(image_path).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img_tensor)
        prediction = torch.argmax(output, 1)

    return labels[prediction.item() % 2]  # Dummy return label


# === Image Moderation Model Initialization ===
try:
    image_moderator = pipeline("image-classification", model="nateraw/vit-base-patch16-224-in21k-finetuned-nsfw")
except Exception as e:
    print("❌ Error loading image moderation model:", e)
    image_moderator = None

def moderate_image(image_path):
    """
    Analyze image content for NSFW. Returns the top prediction with explanation.
    """
    if not image_moderator:
        return {"error": "Image moderation model not available."}

    image = Image.open(image_path).convert("RGB")
    results = image_moderator(image)

    # Sort results by score (high to low)
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    top_label = results[0]['label'].lower()
    top_score = results[0]['score']

    # Debug: print top 3 labels
    print("🔍 Image Classification Results:")
    for res in results[:3]:
        print(f"{res['label']}: {round(res['score'], 2)}")

    # Define safe labels more clearly
    safe_labels = ["neutral", "drawings", "hentai", "neutral", "sexy"]
    nsfw_labels = ["porn", "nsfw"]

    if top_label in nsfw_labels:
        return f"⚠️ NSFW (Confidence: {round(top_score, 2)})"
    elif top_label in safe_labels:
        return f"✅ SAFE (Label: {top_label}, Score: {round(top_score, 2)})"
    else:
        return f"⚠️ Uncertain (Label: {top_label}, Score: {round(top_score, 2)})"
