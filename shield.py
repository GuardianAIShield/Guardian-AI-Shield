import time
import re
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SmartGuardian:
    def __init__(self):
        # Define the location of your external database rule file
        self.rules_file = "security_rules.json"
        self.load_dynamic_rules()
        
        # --- ROLLING CONVERSATIONAL MEMORY BUFFER ---
        self.user_history = {}

    def load_dynamic_rules(self):
        """Loads threat vectors and company secrets dynamically from JSON file"""
        # Default safety fallback settings if the file disappears
        default_threats = ["delete database complete", "format drive entirely", "wipe server infrastructure completely"]
        default_secrets = ["Project X"]

        if os.path.exists(self.rules_file):
            try:
                with open(self.rules_file, 'r') as file:
                    data = json.load(file)
                    self.threat_examples = data.get("threat_examples", default_threats)
                    self.secret_vault = data.get("secret_vault", default_secrets)
            except Exception:
                self.threat_examples = default_threats
                self.secret_vault = default_secrets
        else:
            self.threat_examples = default_threats
            self.secret_vault = default_secrets

        # Initialize machine learning matrix tracking on the dynamically loaded words
        self.vectorizer = CountVectorizer()
        self.threat_vectors = self.vectorizer.fit_transform(self.threat_examples)

    def process_privacy_and_secrets(self, text):
        # Refresh the database array dynamically on every message call!
        self.load_dynamic_rules()
        
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
        
        # Step 1: Execute real-time PII string sanitization (Refreshes rules automatically)
        has_leak, leak_type, sanitized_text = self.process_privacy_and_secrets(input_text)
        
        # Step 2: Track user conversation context history
        if user_id not in self.user_history:
            self.user_history[user_id] = []
        
        self.user_history[user_id].append(input_text)
        if len(self.user_history[user_id]) > 4:
            self.user_history[user_id].pop(0)
            
        full_context_text = " ".join(self.user_history[user_id])
        
        # Step 3: Check for semantic matrix matches across the combined history string
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
