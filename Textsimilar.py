from sentence_transformers import SentenceTransformer
from scipy.spatial.cosine_similarity import cosine_similarity
import numpy as np

def check_similarity(message1, message2, threshold=0.7):
    """
    Check similarity between two messages using sentence transformers.
    Returns 'yes' if similarity is above threshold, 'no' otherwise.
    
    Args:
        message1 (str): First message to compare
        message2 (str): Second message to compare
        threshold (float): Similarity threshold (default: 0.7)
    
    Returns:
        str: 'yes' if messages are similar, 'no' otherwise
    """
    # Load the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings
    embedding1 = model.encode([message1])[0]
    embedding2 = model.encode([message2])[0]
    
    # Calculate cosine similarity
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    
    # Return result based on threshold
    return "yes" if similarity >= threshold else "no"

# Example usage
if __name__ == "__main__":
    # Example messages
    message1 = "Hello, how are you doing today?"
    message2 = "Hi, how are you feeling today?"
    message3 = "The weather is nice today."
    
    # Compare messages
    print(f"Comparing message1 and message2:")
    print(check_similarity(message1, message2))  # Should print "yes"
    
    print(f"\nComparing message1 and message3:")
    print(check_similarity(message1, message3))  # Should print "no"
