import streamlit as st
import openai

# ---------- CONFIG ----------
st.set_page_config(layout="wide")
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# ---------- Initialize State ----------
if "ai_like" not in st.session_state:
    st.session_state.ai_like = "You are an AI assistant that helps users by understanding their entire conversation and replying thoughtfully."
if "show_custom_input" not in st.session_state:
    st.session_state.show_custom_input = False

# ---------- Customize AI Behavior ----------
st.markdown("### ✨ Want a customized AI behavior?")
if st.button("Get Better Experience"):
    st.session_state.show_custom_input = True

if st.session_state.show_custom_input:
    custom_text = st.text_input("Describe how the AI should behave:", key="ai_custom_input")
    if custom_text:
        st.session_state.ai_like = custom_text
        st.session_state.show_custom_input = False  # Hide the input
        st.success("✔️ AI personality updated!")
        st.rerun()  # ✅ Force UI refresh to hide input

# ---------- Chat Memory ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": st.session_state.ai_like}
    ]

# ---------- Top Layout with Clear Button ----------
col1, col2 = st.columns([8, 1])
with col1:
    st.header("💬 Hello, what can I do for you?")
with col2:
    if st.button("🧹 Clear"):
        st.session_state.chjkhuiyuhkjat_history = [
            {"role": "system", "content": st.session_state.ai_like}
        ]
        st.rerun()

# ---------- Display Chat ----------
for msg in st.session_state.chat_history[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

# ---------- CSS: Fixed Input at Bottom ----------
st.markdown("""
    <style>
    .bottom-form {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.15);
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Bottom Input Form ----------
st.markdown('<div class="bottom-form">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    que = st.text_input("Type your message here...", label_visibility="collapsed")
    send = st.form_submit_button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Handle Message ----------
if send and que:
    st.session_state.chat_history.append({"role": "user", "content": que})

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=st.session_state.chat_history
    )
    reply = response['choices'][0]['message']['content']

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()          
