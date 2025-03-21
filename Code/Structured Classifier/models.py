from sentence_transformers import SentenceTransformer, util

# Load SBERT models for both new and bulk classification
new_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
bulk_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Define the label dictionaries
bulk_labels = {
    "1": "Plural items or large quantities of the same item, and"
}

new_labels = {
    "1": "Unopened, unused, new, sealed, or in original packaging."
}

# Compute embeddings for label texts
new_texts = list(new_labels.values())
new_embeddings = new_model.encode(new_texts, normalize_embeddings=True)
bulk_texts = list(bulk_labels.values())
bulk_embeddings = bulk_model.encode(bulk_texts, normalize_embeddings=True)

def classify_sentiments_batch(phrases, model, sentiment_embeddings, sentiment_labels, batch_size=1000, threshold=0.5):
    # Classify sentiments for phrase batches - cosine similarity
    # Return label keys or "uncertain" if below the threshold
    results = []
    label_keys = list(sentiment_labels.keys())
    
    for i in range(0, len(phrases), batch_size):
        batch = phrases[i:i+batch_size]
        batch_embeddings = model.encode(batch, normalize_embeddings=True)
        similarities = util.cos_sim(batch_embeddings, sentiment_embeddings)
        
        for sim in similarities:
            best_match_idx = sim.argmax().item()
            best_match_score = sim[best_match_idx].item()
            if best_match_score < threshold:
                results.append("uncertain")
            else:
                results.append(label_keys[best_match_idx])
    return results
