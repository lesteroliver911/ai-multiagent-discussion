import streamlit as st
import controlflow as cf
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from task import (
    sheldon, leonard, penny, howard, raj, 
    get_topic_context, analyze_sentiment
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="BBT AI Discussion",
    page_icon="🔬",
    layout="wide"
)

# Styling
st.markdown("""
    <style>
    .agent-message {
        padding: 8px;
        border-radius: 4px;
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    .sheldon { background-color: #e3f2fd; }
    .leonard { background-color: #f3e5f5; }
    .penny { background-color: #fff3e0; }
    .howard { background-color: #e8f5e9; }
    .raj { background-color: #fce4ec; }
    .main-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 10px;
    }
    .stMarkdown {
        font-size: 14px;
    }
    .discussion-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%;
        padding: 4px 8px;
        font-size: 14px;
        margin: 2px 0;
        border-radius: 4px;
    }
    div[data-testid="column"] {
        padding: 0 4px;
    }
    .sentiment-indicator {
        font-size: 12px;
        font-style: italic;
        color: #666;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("Big Bang Theory AI Discussion Panel")
st.sidebar.markdown("Watch the BBT gang discuss any topic with their unique perspectives!")
st.sidebar.markdown("<div style='margin-top: -8px;'>---</div>", unsafe_allow_html=True)

st.sidebar.markdown("### Configure Your Discussion")

# Topic input in sidebar
topic = st.sidebar.text_area(
    "Enter a topic for discussion:", 
    key="topic_input",
    height=100  # Initial height in pixels
)

# Character selection in sidebar
st.sidebar.markdown("### Select Characters")
selected_characters = st.sidebar.multiselect(
    "Choose who participates:",
    ["Sheldon", "Leonard", "Penny", "Howard", "Raj"],
    default=["Sheldon", "Leonard", "Penny", "Howard"]
)

# Action buttons in sidebar
st.sidebar.markdown("### Actions")
button_col1, button_col2 = st.sidebar.columns([1, 1])

# Place buttons in columns for better alignment
with button_col1:
    start_button = st.button("Start Discussion", use_container_width=True)
with button_col2:
    continue_button = st.button("Continue", use_container_width=True)

# Clear button spans full width
clear_button = st.sidebar.button("Clear Discussion", use_container_width=True, type="secondary")

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("*dev by [lesteroliver](https://github.com/lesteroliver911)*")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Character mapping
character_map = {
    "Sheldon": sheldon,
    "Leonard": leonard,
    "Penny": penny,
    "Howard": howard,
    "Raj": raj
}

def generate_response(agent, topic, topic_context):
    """Generate a response from an agent"""
    response = cf.run(
        "Contribute to the discussion",
        agents=[agent],
        context={
            "topic": topic,
            "background_info": topic_context
        },
        interactive=False,
        instructions="Respond to the topic and previous comments in character. "
                    "Use the provided background information to make relevant observations. "
                    "Keep responses 1-2 paragraphs max."
    )
    
    # Update to use imported analyze_sentiment
    sentiment_score, sentiment_desc = analyze_sentiment(response)
    
    return {
        "text": response,
        "sentiment_score": sentiment_score,
        "sentiment_desc": sentiment_desc
    }

# Handle Start Discussion
if start_button and topic:
    st.session_state.messages = []
    topic_context = get_topic_context(topic)
    
    with st.spinner('Starting a new discussion...'):
        for char_name in selected_characters:
            agent = character_map[char_name]
            response_data = generate_response(agent, topic, topic_context)
            st.session_state.messages.append({
                "character": char_name, 
                "message": response_data["text"],
                "sentiment_score": response_data["sentiment_score"],
                "sentiment_desc": response_data["sentiment_desc"]
            })

# Handle Continue Discussion
if continue_button and topic and len(st.session_state.messages) > 0:
    topic_context = get_topic_context(topic)
    
    with st.spinner('Generating new responses...'):
        for char_name in selected_characters:
            agent = character_map[char_name]
            response_data = generate_response(agent, topic, topic_context)
            st.session_state.messages.append({
                "character": char_name, 
                "message": response_data["text"],
                "sentiment_score": response_data["sentiment_score"],
                "sentiment_desc": response_data["sentiment_desc"]
            })

# Handle Clear Discussion
if clear_button:
    st.session_state.messages = []
    st.rerun()

# Main content area - only shows messages and info
if st.session_state.messages:
    st.markdown('<p class="discussion-title">Current Discussion: ' + topic + '</p>', unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        # Update to use imported analyze_sentiment
        sentiment_score, sentiment_desc = analyze_sentiment(msg['message'])
        
        st.markdown(
            f"""<div class="agent-message {msg['character'].lower()}">
                <strong>{msg['character']}:</strong> {msg['message']}
                <div class="sentiment-indicator">Sentiment: {sentiment_desc}</div>
            </div>""",
            unsafe_allow_html=True
        )
else:
    st.info("👈 Enter a topic and select characters in the sidebar to start a new discussion!") 