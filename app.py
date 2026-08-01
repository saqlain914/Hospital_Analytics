import streamlit as st
from src.rag.chatbot import ask_hospital_ai

st.set_page_config(page_title="Hospital Analytics", page_icon="🏥", layout="wide")
st.title("🏥 Hospital Operational Intelligence Portal")

# Tab 1: AI Data Assistant
tab1, tab2 = st.tabs(["💬 Ask the Data AI", "🔮 Predict Provider Stay"])

with tab1:
    st.subheader("Talk to your Hospital Database")
    st.caption("The assistant uses a local Ollama model when available; otherwise it shows a friendly fallback message.")
    user_query = st.text_input(
        "Ask a business question:", placeholder="e.g., What is the average billing amount by hospital?"
    )

    if user_query:
        with st.spinner("AI is analyzing records..."):
            answer = ask_hospital_ai(user_query)
            st.write("### 🤖 Response:")
            if "not ready" in answer.lower() or "not reachable" in answer.lower():
                st.warning(answer)
            else:
                st.info(answer)
    else:
        st.info("Enter a question to start the AI assistant.")

with tab2:
    st.subheader("Predict Patient Stay Length")
    st.info("Prediction features will be added here soon.")
    # Add input fields (Age, Medical Condition dropdown, etc.)
    # Load your provider_model.pkl file to show predictions