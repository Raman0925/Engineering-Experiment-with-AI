from email import message
from openai import OpenAI
import streamlit as st
import groq
from google import genai
from core.config import config

def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "OpenAi":
        if not config.OpenAI_API_KEY:
            return "Set OPENAI_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = OpenAI(api_key=config.OpenAI_API_KEY)
    elif provider == "Groq":
        if not config.GROQ_API_KEY:
            return "Set GROQ_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = groq.Groq(api_key=config.GROQ_API_KEY)
    else:
        if not config.GOOGLE_API_KEY:
            return "Set GOOGLE_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = genai.Client(api_key=config.GOOGLE_API_KEY)
    if provider == "Google":
        return client.models.generate_content(model=model_name, contents=[message["content"] for message in messages]).text
    elif provider == "Groq":
        return client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens).choices[0].message.content
    else:
        return client.chat.completions.create(model=model_name, messages=messages, max_tokens=max_tokens).choices[0].message.content
    
with st.sidebar:
    st.title('Settings')

    provider = st.selectbox('Provider', ['OpenAi', 'Groq', 'Google'])
    if provider == 'OpenAi':
        model_name = st.selectbox('Model', ['gpt-4o-mini', 'gpt-4o', 'gpt-4o-turbo'])
    elif provider == 'Groq':
        model_name = st.selectbox('Model', ['llama-3.1-8b-instant', 'llama-3.1-8b-instruct', 'llama-3.1-8b-chat'])
    else:
        model_name = st.selectbox('Model', ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-2.0-flash-lite'])
    

    st.session_state.provider = provider
    st.session_state.model_name = model_name
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': 'Hello! How can I help you today?'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("Hello! How can I help you today?"):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        output = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = output
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({'role': 'assistant', 'content': answer})