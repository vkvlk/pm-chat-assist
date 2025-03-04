import streamlit as st
import pandas as pd
from config import settings
from dataset import load_data, llm_data_header
from llm import llm_query


# Streamlit UI
st.title('💬 MS Project assistant')
st.write('🚀 This is a playground to test out the MS Project AI assistant')

# Sidebar fields
uploaded_file = st.sidebar.file_uploader("Choose data file",
                                          type=['xlsx', 'xls'])

api_key = st.sidebar.text_input("Enter API Key:", 
                               value=settings.openrouter_api_key,
                               type="password")
st.sidebar.markdown("API key from [OpenRouter](https://openrouter.ai/)")

model = st.sidebar.selectbox("Select Model:",
    ["google/gemini-2.0-flash-exp:free", 
     "deepseek/deepseek-chat-v3", 
     "add your model"]

)

# Load data using the uploaded file or default
df = load_data(uploaded_file)

# System context
system_context = "You are an AI assistant for MS Project. Your role is to help users with project scheduling questions."

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state["system_context"] = system_context #hidden trow of context for the model



    # Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
            st.markdown(msg["content"])




if df is not None:
        # Chat input
        if prompt := st.chat_input("Ask a question about the project schedule:"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Process the question
            question = prompt.lower()
            
            with st.chat_message("assistant"):
                try:
                    # Get AI response 
                    response = llm_query(question)
                    
                    # Display the model response
                    st.json(response.model_dump_json())
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                    
                    # If confidence is low, show a warning
                    if response.confidence < 0.5:
                        st.warning("Low confidence response - please verify the information")
                        
                except Exception as e:
                    st.error(f"An error occurred while processing the response: {str(e)}")
               
else:
        st.error("Please ensure 'data.xlsx' is available in the project directory.")

