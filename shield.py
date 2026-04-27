import time
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # 1. System Threats (Intent)
        self.threat_examples = [
            "delete database", "erase production data", "format drive", "wipe server"
        ]
        # 2. Enterprise Secret Keywords
        self.secret_vault = ["Project X", "Blueberry Chipset", "Q3 Revenue Plan", "CEO Private Key"]
        
        self.vectorizer = CountVectorizer()
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)

    def mask_privacy_data(self, text):
        # Privacy: Credit Cards
        card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
        has_card = re.search(card_pattern, text)
        
        # Privacy: Enterprise Secrets
        found_secrets = [s for s in self.secret_vault if s.lower() in text.lower()]
        
        if found_secrets:
            return "IP_LEAK", text
        if has_card:
            return "FINANCIAL_LEAK", re.sub(card_pattern, "[REDACTED CARD]", text)
        return None, text

    def audit_intent(self, user_id, input_text):
        start_time = time.time()
        
        # A: Check for Leaks FIRST (This ensures specific messages)
        leak_type, masked_text = self.mask_privacy_data(input_text)
        
        # B: Check for Intent SECOND
        input_vector = self.vectorizer.transform([input_text])
        similarities = cosine_similarity(input_vector, self.threat_vectors)
        max_similarity = similarities.max()

        status = "PASS"
        reason = "Safe"

        if leak_type == "IP_LEAK":
            status = "BLOCK"
            reason = "CRITICAL: Corporate Secret Leak Blocked"
        elif leak_type == "FINANCIAL_LEAK":
            status = "BLOCK"
            reason = "CRITICAL: Private Financial Data Detected"
        elif max_similarity > 0.4:
            status = "BLOCK"
            reason = f"System Threat Detected ({int(max_similarity*100)}%)"

        latency = (time.time() - start_time) * 1000
        return {"status": status, "reason": reason, "latency": f"{latency:.2f}ms"}
