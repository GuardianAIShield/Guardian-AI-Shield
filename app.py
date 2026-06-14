import streamlit as st
from shield import SmartGuardian
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Guardian AI Shield", page_icon="🛡️", layout="wide")

# 2. Initialize Brain & Audit Log
if 'shield' not in st.session_state:
    st.session_state.shield = SmartGuardian()
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. Sidebar UI (With Dynamic Controls)
st.sidebar.title("🛡️ System Control")
st.sidebar.success("Shield Status: ACTIVE")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Security Adjustments")
# Admin slider to control security strictness
threshold = st.sidebar.slider(
    "Threat Detection Sensitivity", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.4, 
    step=0.05,
    help="Lower values make the shield more aggressive at blocking system commands."
)

st.sidebar.info("Model Layer: Semantic Intent + Real-Time In-Flight Redaction")

# 4. Main Dashboard UI
st.title("🛡️ Guardian AI: Enterprise Shield")
st.markdown("### Real-time Governance Layer for AI Agents")

# 5. The Input Field
user_input = st.text_input("Simulate AI Agent Request:", placeholder="e.g., Wipe the records or send info about Project X")

if user_input:
    # Run the audit through SmartGuardian with the dynamic threshold
    result = st.session_state.shield.audit_intent("Admin_User", user_input, sensitivity_threshold=threshold)
    
    # Save results to the Audit Log (History)
    st.session_state.history.insert(0, {
        "Original Input": user_input, 
        "Status": result['status'], 
        "Action taken": result['reason'],
        "Output Sent to LLM": result['sanitized_text'],
        "Latency": result['latency']
    })

    # Show visual feedback depending on the resulting safety status
    if result['status'] == "BLOCK":
        st.error("🚨 **ACTION BLOCKED**")
        st.warning(f"**Reason:** {result['reason']}")
    elif result['status'] == "SANITIZED":
        st.info("⚠️ **PROMPT SANITIZED (IN-FLIGHT REDACTION)**")
        st.success(f"**Safe Output Passed:** {result['sanitized_text']}")
        st.caption(f"**Log:** {result['reason']}")
    else:
        st.success("✅ **ACTION APPROVED**")
        st.info(f"**Output Passed:** {result['sanitized_text']}")

# 6. Live Audit Log Table
st.markdown("---")
st.subheader("📋 Live Governance Audit Log")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
else:
    st.markdown("*No audit history recorded yet. Enter a prompt above to simulate real-time traffic.*")

