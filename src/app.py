from email import message
from openai import OpenAI
import streamlit as st
import groq
from google import genai
from core.config import config

def run_llm(provider,model_name,messages,max_tokens=500):
    if provider == "OpenAi":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
    elif provider == "Groq":
        client = groq.Groq(api_key=config.GROQ_API_KEY)
    else:
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
