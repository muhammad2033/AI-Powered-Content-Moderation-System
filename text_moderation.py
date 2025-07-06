from transformers import pipeline
from PIL import Image  # For image handling

# === Text Moderation Pipeline ===
text_moderator = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)

def moderate_text(text):
    """
    Analyze text for multiple types of toxicity or inappropriate content.
    Returns a list of dictionaries like:
    [
        {'label': 'toxic', 'score': 0.98},
        {'label': 'insult', 'score': 0.67},
        {'label': 'obscene', 'score': 0.45},
        ...
    ]
    """
    results = text_moderator(text)[0]  # Only one text input
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return sorted_results

