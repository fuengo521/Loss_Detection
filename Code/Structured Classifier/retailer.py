import re
import pandas as pd
from thefuzz import fuzz, process

def normalize_text(text):
    # Normalize text: lower case, remove punctuation and white space
    if pd.isna(text):
        return None
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[^\w\s]', '', text.lower().strip())
    return ' '.join(text.split())

def find_best_match(text, choices, threshold=70, original_choices=None):
    # Find the best matching retailer - fuzzy matching
    # Return original retailer name if good match is found
    if pd.isna(text) or not isinstance(text, str):
        return None
    
    text_normalized = normalize_text(text)
    match = process.extractOne(text_normalized, choices, scorer=fuzz.token_set_ratio)
    
    if match and match[1] >= threshold:
        # Use original retailer names for display if provided
        if original_choices:
            original_store = [s for s in original_choices if normalize_text(s) == match[0]][0]
        else:
            original_store = match[0]
        return original_store
    return None
