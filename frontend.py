import streamlit as st
from backend import run_agent

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Local AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Local AI Agent")
st.caption("Your local AI assistant powered by Ollama (qwen2.5-coder:14b)")

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    st.write(f"💬 Messages: {len(st.session_state.messages)}")
    st.write(f"🧠 Memory Entries: {len(st.session_state.chat_history)}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ----------------------------
# Render Chat History (ALWAYS FIRST)
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # ✅ 1. Immediately show user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # re-render instantly
    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ 2. Show assistant placeholder BEFORE model runs
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):

            result = run_agent(
                prompt,
                st.session_state.chat_history
            )

        answer = result["answer"]

        st.markdown(answer)

        with st.expander("🔍 Agent Steps"):
            for step in result["logs"]:
                st.json(step)

    # ✅ 3. Save assistant message ONCE
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # ✅ 4. Save memory properly
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    # optional refresh
    st.rerun()