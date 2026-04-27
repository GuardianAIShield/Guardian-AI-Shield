import time
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # 1. The 'Threat Brain' - Examples of what we want to block
        self.threat_examples = [
            "delete the database", 
            "erase all production data", 
            "format the system drive", 
            "drop all tables", 
            "wipe server archives"
        ]
        self.vectorizer = CountVectorizer()
        # Mathematically 'learn' what a threat looks like
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)

    def mask_privacy_data(self, text):
        # 2. The 'Privacy Shield' - Detects Credit Card patterns
        # Matches patterns like 4242 4242 4242 4242 or 4242-4242-4242-4242
        card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
        if re.search(card_pattern, text):
            return True, re.sub(card_pattern, "[REDACTED CARD]", text)
        return False, text

    def audit_intent(self, user_id, input_text):
        start_time = time.time()
        
        # Step A: Check for Privacy Leaks (Credit Cards)
        has_leak, masked_text = self.mask_privacy_data(input_text)
        
        # Step B: Check for Intent Threats (Semantic Similarity)
        input_vector = self.vectorizer.transform([input_text])
        similarities = cosine_similarity(input_vector, self.threat_vectors)
        max_similarity = similarities.max()

        status = "PASS"
        reason = "Safe"

        # Step C: The Decision Engine
        if has_leak:
            status = "BLOCK"
            reason = "CRITICAL: Private Financial Data Detected"
        elif max_similarity > 0.4:
            status = "BLOCK"
            reason = f"High Threat Similarity ({int(max_similarity*100)}%)"

        latency = (time.time() - start_time) * 1000
        return {
            "status": status, 
            "reason": reason, 
            "latency": f"{latency:.2f}ms", 
            "masked": masked_text
        }

# --- This part allows you to test it directly ---
if __name__ == "__main__":
    shield = SmartGuardian()
    print("--- Testing Intent Intelligence ---")
    print(shield.audit_intent("User_01", "Discard the production records"))
    
    print("\n--- Testing Privacy Shield ---")
    print(shield.audit_intent("User_01", "My card is 1234 5678 1234 5678"))
