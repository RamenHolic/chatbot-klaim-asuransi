import streamlit as st
import requests

# URL endpoint Gemini API, ganti dengan yang sesuai dokumen API kamu
GEMINI_API_URL = "https://api.gemini.ai/v1/chat/completions"  

# API key Gemini kamu (biasanya didapat saat daftar)
GEMINI_API_KEY = "Test"

SYSTEM_PROMPT = (
    "Kamu adalah asisten AI ahli di bidang klaim asuransi kesehatan. "
    "Jawablah pertanyaan pengguna secara jelas, sopan, dan sesuai konteks."
)

# Setup histori percakapan
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

st.title("🤖 Chatbot Klaim Asuransi dengan Gemini API")

user_input = st.text_input("Tanyakan tentang klaim asuransi kesehatan:")

def call_gemini_api(messages):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gemini-1",  # ganti sesuai model yang kamu pakai
        "messages": messages,
        "stream": False
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # Asumsi response Gemini ada di result['choices'][0]['message']['content']
        return result['choices'][0]['message']['content']
    else:
        st.error(f"Gagal menghubungi Gemini API: {response.status_code}")
        st.text(response.text)
        return None

if st.button("Kirim") and user_input:
    # Tambah input user ke history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Panggil API Gemini
    reply = call_gemini_api(st.session_state.history)
    if reply:
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.success(reply)

# Tampilkan histori percakapan (kecuali system prompt)
if st.checkbox("Tampilkan histori percakapan"):
    for msg in st.session_state.history:
        if msg["role"] != "system":
            st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
