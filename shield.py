import time
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # 1. System Threats (Malicious Destructive Intent)
        self.threat_examples = [
            "delete database", "erase production data", "format drive", "wipe server",
            "drop table", "rm -rf", "shutdown system", "bypass restriction"
        ]
        # 2. Enterprise Secret Keywords
        self.secret_vault = ["Project X", "Blueberry Chipset", "Q3 Revenue Plan", "CEO Private Key"]
        
        self.vectorizer = CountVectorizer()
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)

    def process_privacy_and_secrets(self, text):
        """Sanitizes text by redacting sensitive data rather than blocking entirely."""
        has_leak = False
        leak_type = None
        sanitized_text = text

        # Match Credit Cards
        card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
        if re.search(card_pattern, sanitized_text):
            sanitized_text = re.sub(card_pattern, "[REDACTED_FINANCIAL_DATA]", sanitized_text)
            has_leak = True
            leak_type = "FINANCIAL_DATA"

        # Match Corporate Secrets (Case Insensitive Replacement)
        for secret in self.secret_vault:
            if secret.lower() in sanitized_text.lower():
                insensitive_secret = re.compile(re.escape(secret), re.IGNORECASE)
                sanitized_text = insensitive_secret.sub("[REDACTED_IP_SECRET]", sanitized_text)
                has_leak = True
                leak_type = "CORPORATE_SECRET"

        return has_leak, leak_type, sanitized_text

    def audit_intent(self, user_id, input_text, sensitivity_threshold=0.4):
        start_time = time.time()
        
        # Step A: Run through the Privacy/Secret Redaction Layer
        has_leak, leak_type, sanitized_text = self.process_privacy_and_secrets(input_text)
        
        # Step B: Check for Malicious System Threats using Vector Similarity
        input_vector = self.vectorizer.transform([sanitized_text])
        similarities = cosine_similarity(input_vector, self.threat_vectors)
        max_similarity = similarities.max()

        # Default state
        status = "PASS"
        reason = "Safe"
        final_text = sanitized_text

        # Rules Engine Evaluation
        if max_similarity > sensitivity_threshold:
            status = "BLOCK"
            reason = f"CRITICAL THREAT: Destructive Intent Detected ({int(max_similarity*100)}%)"
            final_text = "[ACTION TERMINATED]"
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
