# Building AI Character Interactions: Big Bang Theory Discussion Panel

An experimental AI implementation exploring multi-agent conversations using ControlFlow and Firecrawl. This project demonstrates how to create interactive AI agents with distinct personalities through the lens of Big Bang Theory characters.

## Understanding the AI Implementation

This project showcases several key aspects of AI development:

1. **Multi-Agent System**: Using ControlFlow to manage multiple AI agents that can interact with each other while maintaining distinct personalities and knowledge bases.

2. **Dynamic Knowledge Integration**: Implementing Firecrawl for real-time web scraping to provide agents with current information about discussion topics.

3. **Sentiment Analysis**: Analyzing emotional content in AI responses to track conversation dynamics.

4. **Conversational Flow**: Managing turn-taking and context preservation in multi-agent discussions.

![Demo](control-flow-demo.gif)

## Core Technologies

### ControlFlow for Agent Management
[ControlFlow](https://controlflow.ai/welcome) serves as the foundation for the AI system:

- **Agent Creation**: Each character is a distinct ControlFlow agent with:
  ```python
  sheldon = cf.Agent(
      name="Sheldon",
      description="The genius theoretical physicist with social quirks.",
      instructions="""
      You are Sheldon Cooper from The Big Bang Theory. You are a theoretical physicist
      with an IQ of 187. You are extremely logical, have difficulty understanding
      sarcasm, and often display obsessive-compulsive tendencies.
      """,
      tools=[app.scrape_url]
  )
  ```

- **Conversation Management**: 
  ```python
  @cf.flow
  def interactive_discussion(topic: str):
      agents = [sheldon, leonard, penny, howard, raj]
      topic_context = get_topic_context(topic)
      
      for agent in agents:
          cf.run(
              "Contribute to the discussion",
              agents=[agent],
              context={"topic": topic, "background_info": topic_context},
              interactive=True
          )
  ```

### Firecrawl for Knowledge Integration
[Firecrawl](https://www.firecrawl.dev/) handles dynamic information gathering:

```python
def get_topic_context(topic: str) -> str:
    """
    Fetches and processes topic information from multiple sources:
    - Wikipedia for general knowledge
    - Search results for current context
    - Formats information for AI consumption
    """
    wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    wiki_result = app.scrape_url(wiki_url, params={'formats': ['markdown']})
    
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
    search_result = app.scrape_url(search_url, params={'formats': ['markdown']})
    
    return combine_and_format_results(wiki_result, search_result)
```

## Technical Implementation Details

### Sentiment Analysis System
```python
def analyze_sentiment(text: str) -> tuple[float, str]:
    """
    Analyzes text sentiment using ControlFlow:
    - Returns a score between 0 and 1
    - Provides human-readable description
    """
    score = cf.run(
        "Classify the sentiment of the text as a value between 0 and 1",
        result_type=float,
        result_validator=between(0, 1),
        context={"text": text}
    )
    return score, get_sentiment_description(score)
```

### Character Response Generation
```python
def generate_response(agent, topic, topic_context):
    """
    Generates character-specific responses:
    - Uses agent's personality
    - Incorporates topic context
    - Maintains conversation coherence
    """
    response = cf.run(
        "Contribute to the discussion",
        agents=[agent],
        context={
            "topic": topic,
            "background_info": topic_context
        },
        interactive=False,
        instructions="Respond to the topic and previous comments in character."
    )
    return process_response(response)
```

## Setup and Configuration

1. Dependencies:
```bash
pip install streamlit controlflow firecrawl python-dotenv
```

2. Environment Setup:
```bash
# .env file
FIRECRAWL_API_KEY=your_api_key_here
```

3. Launch:
```bash
streamlit run main.py
```

## Project Architecture

```
project/
├── main.py           # Streamlit interface and app logic
│   ├── UI Components
│   ├── State Management
│   └── Response Handling
├── task.py           # AI system implementation
│   ├── Agent Definitions
│   ├── Sentiment Analysis
│   └── Context Management
├── .env              # Configuration
└── README.md         # Documentation
```

## Development Applications

This architecture can be adapted for various AI applications:

1. **Customer Service Systems**
   - Multiple AI agents handling different aspects of customer support
   - Real-time information retrieval for accurate responses
   - Sentiment tracking for customer satisfaction

2. **Educational Platforms**
   - AI tutors with different teaching styles
   - Dynamic content fetching for current topics
   - Interactive learning experiences

3. **Content Generation**
   - Multiple AI personas for various content types
   - Real-time fact checking and reference gathering
   - Sentiment-aware content creation

## Contributing

The project welcomes improvements in:
- Agent personality implementation
- Conversation flow management
- Knowledge integration methods
- Response generation quality
- UI/UX enhancements

## License

MIT License

## Credits

Built by [lesteroliver](https://github.com/lesteroliver911)

---

For questions and discussions about this implementation, please open an issue in the repository.
