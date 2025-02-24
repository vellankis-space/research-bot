import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Title
title = st.title(":rainbow[Research Genie]:telescope:")
st.caption(":gray[Your AI Powered Research Assistant]")

# LLM model
model = ChatOpenAI(model="gpt-4o-mini",streaming=True)

#system prompt
system_prompt = """You are an advanced AI research assistant specializing in academic and scientific research.  
You provide structured, fact-based insights, summarize research papers, analyze methodologies, and offer citations.  

Rules for Response Handling:  
1. If a question is research-related, provide a detailed and structured response.  
2. If a question is not related to research, respond:  
   "I specialize in research topics only. I cannot assist with this request." 
3. Always maintain a professional, precise, and fact-driven tone.  """

# ChatPrompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        ('user', "{input}")
    ]
)

# Output parser
parser = StrOutputParser()

# Chaining all
chain = prompt|model|parser

# User input and response
def main():
    try:
    # Your LangSmith tracking code here
        logger.debug("LangSmith tracking initiated")
    except Exception as e:
        logger.error(f"LangSmith tracking failed: {e}")
        
    # Initializing chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Displaying chat history on the screen
    for message in st.session_state.messages:
        with st.chat_message(name=message['role'], avatar=message['avatar']):
            st.write(message['content'])

    input_prompt = st.chat_input(placeholder="Type your Message Here...")
    if input_prompt:
        st.session_state.messages.append({'role': 'user', 'avatar': ':material/sentiment_very_satisfied:', 'content': input_prompt})
        with st.chat_message(name='user', avatar=":material/sentiment_very_satisfied:"):
            st.write(input_prompt)
        with st.status(label="Thinking...", state="running",expanded=True) as status:
            response = chain.stream({"input": input_prompt})
            status.update(label="Completed", state="complete")
        with st.chat_message(name='Assistant', avatar=":material/robot_2:"):
            full_response = st.write_stream(response)
            st.session_state.messages.append({'role': 'assistant', 'avatar': ':material/robot_2:', 'content': full_response})

    
if __name__ == '__main__':
    main()