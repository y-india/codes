import streamlit as st
import requests
import os

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("AI Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "google/gemma-3n-e4b-it:free",
                    "messages": st.session_state.messages
                }
            )

            data = response.json()

            if response.status_code != 200:
                st.error("API error")
                st.json(data)
            else:
                answer = data["choices"][0]["message"]["content"]
                st.write(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )



