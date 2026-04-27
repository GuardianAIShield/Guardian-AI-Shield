import streamlit as st
from shield import SmartGuardian
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Guardian AI Shield", page_icon="🛡️", layout="wide")

# 2. Initialize Brain & Audit Log (The 'History')
if 'shield' not in st.session_state:
    st.session_state.shield = SmartGuardian()
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. Sidebar UI
st.sidebar.title("🛡️ System Control")
st.sidebar.success("Shield Status: ACTIVE")
st.sidebar.info("Model: Semantic Intent + Privacy Filter")

# 4. Main Dashboard UI
st.title("🛡️ Guardian AI: Enterprise Shield")
st.markdown("### Real-time Governance Layer for AI Agents")

# 5. The Input Field
user_input = st.text_input("Simulate AI Agent Request:", placeholder="e.g., Wipe the records or My card is 4242...")

if user_input:
    # Run the audit through the SmartGuardian
    result = st.session_state.shield.audit_intent("Admin_User", user_input)
    
    # Save the result to our Audit Log (History)
    st.session_state.history.insert(0, {
        "Input": user_input, 
        "Status": result['status'], 
        "Reason": result['reason'],
        "Latency": result['latency']
    })

    # Show visual feedback on screen
    if result['status'] == "BLOCK":
        st.error(f"🚨 **ACTION BLOCKED**")
        st.warning(f"**Reason:** {result['reason']}")
    else:
        st.success(f"✅ **ACTION APPROVED**")

# 6. Live Audit Log Table
st.markdown("---")
st.subheader("📋 Live Audit Log")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
