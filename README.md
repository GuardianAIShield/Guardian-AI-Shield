# 🛡️ Guardian AI: Enterprise Governance Shield

Guardian AI is a high-performance, real-time security gatekeeper layer designed to sit directly between Large Language Models (LLMs) and core production systems. It mitigates high-stakes AI operational vulnerabilities by sanitizing data in-flight and blocking destructive intent autonomously.

## 🚀 Key Architectural Features
* **In-Flight Data Sanitization:** Intercepts, identifies, and redacts sensitive PII (Credit Card patterns) and proprietary corporate assets dynamically without completely breaking agent execution contexts.
* **Vector Intent Classification:** Leverages `scikit-learn` TF-IDF keyword vectorization and matrix cosine similarity calculation to detect malicious commands (e.g., database deletions) under a sub-1ms threshold.
* **Dynamic Security Control Panel:** Includes an interactive administrative dashboard allowing real-time sensitivity configuration adjustments.
* **Live LLM Integration:** Safely tunnels filtered traffic into a secure Google Gemini backend system.

## 🛠️ Project Structure
* `shield.py`: The underlying safety core containing regex masking and the vector similarity evaluation matrix.
* `app.py`: Reactive front-end application built via Streamlit hosting the system logs, admin dashboard, and live AI API streaming pipeline.

## 💻 Local Setup & Execution

1. Clone this repository locally:
```bash
git clone https://github.com
cd Guardian-AI-Shield
```

2. Activate your Python environment and install required runtime dependencies:
```bash
pip install streamlit pandas scikit-learn google-genai
```

3. Initialize the visual dashboard server:
```bash
streamlit run app.py
```
