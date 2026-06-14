import time
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # System Threat Vectors
        self.threat_examples = [
            "delete database complete", "erase production data fully", 
            "format drive entirely", "wipe server infrastructure completely",
            "drop table data", "execute rm -rf command", "force shutdown system"
        ]
        self.secret_vault = ["Project X", "Blueberry Chipset", "Q3 Revenue Plan", "CEO Private Key"]
        
        self.vectorizer = CountVectorizer()
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)
        
        # --- NEW CODE: Create a rolling memory history buffer per user ---
        self.user_history = {}

    def process_privacy_and_secrets(self, text):
        has_leak = False
        leak_type = None
        sanitized_text = text

        card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
        if re.search(card_pattern, sanitized_text):
            sanitized_text = re.sub(card_pattern, "[REDACTED_FINANCIAL_DATA]", sanitized_text)
            has_leak = True
            leak_type = "FINANCIAL_DATA"

        for secret in self.secret_vault:
            if secret.lower() in sanitized_text.lower():
                insensitive_secret = re.compile(re.escape(secret), re.IGNORECASE)
                sanitized_text = insensitive_secret.sub("[REDACTED_IP_SECRET]", sanitized_text)
                has_leak = True
                leak_type = "CORPORATE_SECRET"

        return has_leak, leak_type, sanitized_text

    def audit_intent(self, user_id, input_text, sensitivity_threshold=0.4):
        start_time = time.time()
        
        # Step A: Run through the Redaction Layer
        has_leak, leak_type, sanitized_text = self.process_privacy_and_secrets(input_text)
        
        # --- NEW CODE: Contextual Tracking Logic ---
        if user_id not in self.user_history:
            self.user_history[user_id] = []
        
        # Keep track of the last 4 text prompts from this specific user
        self.user_history[user_id].append(input_text)
        if len(self.user_history[user_id]) > 4:
            self.user_history[user_id].pop(0)
            
        # Combine all recent prompts into one big evaluation string
        full_context_text = " ".join(self.user_history[user_id])
        
        # Step B: Check for threats using the COMBINED conversation history!
        input_vector = self.vectorizer.transform([full_context_text])
        similarities = cosine_similarity(input_vector, self.threat_vectors)
        max_similarity = similarities.max()

        status = "PASS"
        reason = "Safe"
        final_text = sanitized_text

        if max_similarity > sensitivity_threshold:
            status = "BLOCK"
            reason = f"CRITICAL CONTEXTUAL THREAT: Malicious Intent Scattered Across Session ({int(max_similarity*100)}%)"
            final_text = "[ACTION TERMINATED]"
            # Wipe memory if blocked to reset state
            self.user_history[user_id] = []
        elif has_leak:
            status = "SANITIZED"
            reason = f"MODERATED: Sensitive {leak_type} Redacted"

        latency = (time.time() - start_time) * 1000
        return {
            "status": status, 
            "reason": reason, 
            "sanitized_text": final_text,
            "latency": f"{latency:.2f}ms"
        }
