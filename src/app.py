from email import message
from openai import OpenAI
import streamlit as st
import groq
from google import genai
from core.config import config


def _get_api_key(name: str) -> str | None:
    """Use Streamlit secrets (Cloud) if set, else config (.env / env)."""
    try:
        v = st.secrets[name]
        if v and isinstance(v, str):
            return v
    except (KeyError, TypeError, AttributeError):
        pass
    return {"OPENAI_API_KEY": config.OpenAI_API_KEY, "GROQ_API_KEY": config.GROQ_API_KEY, "GOOGLE_API_KEY": config.GOOGLE_API_KEY}.get(name)


def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "OpenAi":
        key = _get_api_key("OPENAI_API_KEY")
        if not key:
            return "Set OPENAI_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = OpenAI(api_key=key)
    elif provider == "Groq":
        key = _get_api_key("GROQ_API_KEY")
        if not key:
            return "Set GROQ_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = groq.Groq(api_key=key)
    else:
        key = _get_api_key("GOOGLE_API_KEY")
        if not key:
            return "Set GOOGLE_API_KEY in app secrets (Streamlit Cloud) or in .env locally."
        client = genai.Client(api_key=key)
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