import streamlit as st
from shield import SmartGuardian
import pandas as pd
from google import genai
import os

# 1. Page Configuration
st.set_page_config(page_title="Guardian AI Shield", page_icon="🛡️", layout="wide")

# 2. Initialize Brain, Audit Log, and API Key Entry
if 'shield' not in st.session_state:
    st.session_state.shield = SmartGuardian()
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. Sidebar UI (With Dynamic Controls + API Key Input)
st.sidebar.title("🛡️ System Control")
st.sidebar.success("Shield Status: ACTIVE")

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 LLM Backend Configuration")
# Input box for your Gemini API key (hidden for safety)
gemini_key = st.sidebar.text_input("Enter Gemini API Key:", type="password", help="Get a free key from Google AI Studio")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Security Adjustments")
threshold = st.sidebar.slider(
    "Threat Detection Sensitivity", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.4, 
    step=0.05
)

# 4. Main Dashboard UI
st.title("🛡️ Guardian AI: Enterprise Shield")
st.markdown("### Real-time Governance Layer with Live LLM Integration")

# 5. The Input Field
user_input = st.text_input("Simulate AI Agent Request:", placeholder="e.g., Tell me a story or send info about Project X")

if user_input:
    # Run the audit through SmartGuardian with the dynamic threshold
    result = st.session_state.shield.audit_intent("Admin_User", user_input, sensitivity_threshold=threshold)
    
    # Show visual security feedback depending on the safety status
    if result['status'] == "BLOCK":
        st.error("🚨 **ACTION BLOCKED**")
        st.warning(f"**Reason:** {result['reason']}")
        llm_response = "[BLOCKED BY GOVERNANCE POLICY]"
        
    elif result['status'] == "SANITIZED" or result['status'] == "PASS":
        if result['status'] == "SANITIZED":
            st.info("⚠️ **PROMPT SANITIZED (IN-FLIGHT REDACTION)**")
            st.success(f"**Safe Output Passed:** {result['sanitized_text']}")
        else:
            st.success("✅ **ACTION APPROVED**")
            
        # --- NEW CODE: SEND THE SAFE TEXT TO THE LIVE LLM ---
        if gemini_key:
            try:
                st.markdown("---")
                with st.spinner("🧠 LLM is thinking..."):
                    # Initialize the client with the provided key
                    client = genai.Client(api_key=gemini_key)
                    # Pass the *sanitized_text* instead of the dangerous raw user input!
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=result['sanitized_text'],
                    )
                    llm_response = response.text
                    
                st.subheader("🤖 Live AI Response:")
                st.info(llm_response)
            except Exception as e:
                st.error(f"Failed to call Gemini API: {e}")
                llm_response = "[API ERROR]"
        else:
            st.warning("👉 Please enter your Gemini API Key in the sidebar to view live AI responses!")
            llm_response = "[MISSING API KEY]"

    # Save results to the Audit Log (History)
    st.session_state.history.insert(0, {
        "Original Input": user_input, 
        "Status": result['status'], 
        "Action taken": result['reason'],
        "Output Sent to LLM": result['sanitized_text'],
        "LLM Final Response": llm_response,
        "Latency": result['latency']
    })

# 6. Live Audit Log Table
st.markdown("---")
st.subheader("📋 Live Governance Audit Log")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
