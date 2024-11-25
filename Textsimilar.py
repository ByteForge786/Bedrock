from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np

def preprocess_text(text):
    """
    Preprocess the text by converting to lowercase and removing special characters
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return text

def calculate_similarity(text1, text2, threshold=0.5):
    """
    Calculate cosine similarity between two texts
    Args:
        text1 (str): First text
        text2 (str): Second text
        threshold (float): Similarity threshold (default: 0.5)
    Returns:
        tuple: (similarity_score, is_similar)
    """
    # Preprocess texts
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the texts
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
    except ValueError as e:
        print(f"Error: {e}")
        return 0.0, False
    
    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Determine if texts are similar based on threshold
    is_similar = similarity >= threshold
    
    return similarity, is_similar

# Example usage
if __name__ == "__main__":
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The fast brown fox leaps over the sleepy dog"
    
    similarity_score, is_similar = calculate_similarity(text1, text2)
    print(f"Similarity score: {similarity_score:.2f}")
    print(f"Are texts similar? {'Yes' if is_similar else 'No'}")
