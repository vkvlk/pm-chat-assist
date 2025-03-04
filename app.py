import streamlit as st
from config import settings
from dataset import load_and_format_data
from llm import classify_question






# Streamlit UI
st.title('MS Project assistant')
st.write('This is a playground to test out the MS Project AI assistant')

# Sidebar fields
uploaded_file = st.sidebar.file_uploader("Choose data file",
                                          type=['xlsx', 'xls'])

api_key = st.sidebar.text_input("Enter API Key:", 
                               value=settings.openrouter_api_key,
                               type="password")
st.sidebar.markdown("API key from [OpenRouter](https://openrouter.ai/)")


model = st.sidebar.selectbox(
    "Select Model:",
    ["google/gemini-2.0-flash-exp:free", 
     "deepseek/deepseek-chat-v3", 
     "add your model"]

)





