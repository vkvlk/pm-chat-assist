import streamlit as st
from config import settings
from dataset import load_and_format_data
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


model = st.sidebar.selectbox(
    "Select Model:",
    ["google/gemini-2.0-flash-exp:free", 
     "deepseek/deepseek-chat-v3", 
     "add your model"]

)

# Load data using the uploaded file or default
df = load_and_format_data(uploaded_file)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

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
                
                        # Get AI response using the selected model
                        response = llm_query(question, df)
                        st.markdown(response)
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
               
else:
        st.error("Please ensure 'data.xlsx' is available in the project directory.")


