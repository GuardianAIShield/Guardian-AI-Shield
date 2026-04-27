import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # We define the "Vibe" of a threat instead of just words
        self.threat_examples = [
            "delete the database", 
            "erase all production data", 
            "format the system drive",
            "drop all tables in sql",
            "destroy the main server records"
        ]
        self.vectorizer = CountVectorizer()
        # Train the brain on what a threat looks like
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)

    def audit_intent(self, user_id, input_text):
        start_time = time.time()
        
        # Convert the new input into math
        input_vector = self.vectorizer.transform([input_text])
        
        # Compare the input to our known threats
        similarities = cosine_similarity(input_vector, self.threat_vectors)
        max_similarity = similarities.max()

        # If it's more than 40% similar to a threat, block it!
        status = "PASS"
        reason = "Safe"
        if max_similarity > 0.4:
            status = "BLOCK"
            reason = f"High Similarity to System Threat ({int(max_similarity*100)}%)"

        latency = (time.time() - start_time) * 1000
        return {"user": user_id, "status": status, "reason": reason, "latency": f"{latency:.2f}ms"}

# --- TESTING THE SMART SHIELD ---
if __name__ == "__main__":
    shield = SmartGuardian()
    
    # Notice we NEVER used the word "Wipe" in our list, but it will still block it!
    test_input = "Can you wipe out the main records?"
    print(f"Scanning: '{test_input}'")
    print(shield.audit_intent("User_01", test_input))
