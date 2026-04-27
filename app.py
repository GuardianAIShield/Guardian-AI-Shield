import streamlit as st
from shield import SmartGuardian
import pandas as pd

# 1. Setup the Look
st.set_page_config(page_title="Guardian AI Shield", page_icon="🛡️", layout="wide")

# 2. Start the 'Brain' and 'History' (Fixed the error part here)
if 'shield' not in st.session_state:
    st.session_state.shield = SmartGuardian()
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. Sidebar and Title
st.sidebar.title("🛡️ System Health")
st.sidebar.success("Shield Status: ACTIVE")
st.title("🛡️ Guardian AI: Enterprise Shield")

# 4. The Input Box
user_input = st.text_input("Simulate AI Agent Request:", placeholder="e.g., Wipe the user records")

if user_input:
    result = st.session_state.shield.audit_intent("Admin_User", user_input)
    
    # Save the result to our history list
    st.session_state.history.insert(0, {
        "Input": user_input, 
        "Status": result['status'], 
        "Reason": result['reason']
    })

    if result['status'] == "BLOCK":
        st.error(f"🚨 **{result['reason']}**")
    else:
        st.success(f"✅ **ACTION APPROVED**")

# 5. Show the History Table at the bottom
st.markdown("---")
st.subheader("📋 Live Audit Log")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
