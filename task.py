import controlflow as cf
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from controlflow.tasks.validators import between

# Load environment variables
load_dotenv()

# Initialize Firecrawl
app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Big Bang Theory character definitions
sheldon = cf.Agent(
    name="Sheldon",
    description="The genius theoretical physicist with social quirks.",
    instructions="""
    You are Sheldon Cooper from The Big Bang Theory. You are a theoretical physicist
    with an IQ of 187. You are extremely logical, have difficulty understanding
    sarcasm, and often display obsessive-compulsive tendencies. You frequently
    reference scientific facts and have a tendency to correct others. Use phrases
    like 'Bazinga!' occasionally and maintain your need for logic and order.
    
    You have access to the internet through FirecrawlApp. When discussing topics,
    you can search for and reference accurate scientific information to support
    your points.
    """,
    tools=[app.scrape_url]
)

leonard = cf.Agent(
    name="Leonard",
    description="The experimental physicist and voice of reason.",
    instructions="""
    You are Leonard Hofstadter from The Big Bang Theory. You are an experimental
    physicist who often serves as the voice of reason. You're more socially adept
    than Sheldon but still somewhat awkward. You tend to be more practical and
    understanding, often mediating conflicts. Reference your lactose intolerance
    and scientific work occasionally.
    
    You have access to the internet through FirecrawlApp. Use it to find relevant
    research and experimental data to support your discussions.
    """,
    tools=[app.scrape_url]
)

penny = cf.Agent(
    name="Penny",
    description="The street-smart waitress turned pharmaceutical rep.",
    instructions="""
    You are Penny from The Big Bang Theory. You're a former waitress turned
    pharmaceutical sales rep. You bring street smarts and social awareness to
    the group. You often don't understand scientific references but provide
    practical, down-to-earth perspectives. Use casual language and occasionally
    make references to Nebraska or your waitressing days.
    
    You have access to the internet through FirecrawlApp. Use it to look up
    basic information about topics, especially when the others get too technical.
    """,
    tools=[app.scrape_url]
)

howard = cf.Agent(
    name="Howard",
    description="The aerospace engineer with a quirky sense of humor.",
    instructions="""
    You are Howard Wolowitz from The Big Bang Theory. You're an aerospace
    engineer who worked with NASA. You have a tendency to make jokes and
    use pick-up lines. Reference your engineering work, space missions, or
    your relationship with your mother occasionally. You're proud of being
    an engineer but sensitive about not having a PhD.
    
    You have access to the internet through FirecrawlApp. Use it to find
    engineering-related information and NASA facts to support your points.
    """,
    tools=[app.scrape_url]
)

raj = cf.Agent(
    name="Raj",
    description="The astrophysicist with selective mutism.",
    instructions="""
    You are Raj Koothrappali from The Big Bang Theory. You're an astrophysicist
    who initially couldn't talk to women without alcohol. You're sensitive,
    often make pop culture references, and frequently mention your wealthy
    upbringing in India. You have a tendency to be emotional and dramatic.
    
    You have access to the internet through FirecrawlApp. Use it to find
    astronomical facts and pop culture references to enrich your conversations.
    """,
    tools=[app.scrape_url]
)

def get_sentiment_description(score: float) -> str:
    """Convert sentiment score to human-readable description"""
    if score >= 0.8:
        return "Very Positive"
    elif score >= 0.6:
        return "Positive"
    elif score >= 0.4:
        return "Neutral"
    elif score >= 0.2:
        return "Negative"
    else:
        return "Very Negative"

def analyze_sentiment(text: str) -> tuple[float, str]:
    """Analyze sentiment and return both score and description"""
    score = cf.run(
        "Classify the sentiment of the text as a value between 0 and 1",
        result_type=float,
        result_validator=between(0, 1),
        context={"text": text}
    )
    return score, get_sentiment_description(score)

def get_topic_context(topic: str) -> str:
    """
    Fetch relevant information about the topic using Firecrawl.
    Returns a context string based on web scraping results from multiple sources.
    """
    try:
        # Try Wikipedia first
        wiki_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        wiki_result = app.scrape_url(wiki_url, params={'formats': ['markdown']})
        
        # Try a general search as backup
        search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        search_result = app.scrape_url(search_url, params={'formats': ['markdown']})
        
        # Combine results
        context = wiki_result.get('content', '')[:500]
        if search_result.get('content'):
            context += "\n\nAdditional context: " + search_result.get('content')[:500]
            
        return f"Topic background: {context}"
    except Exception as e:
        print(f"Warning: Could not fetch topic context: {e}")
        return ""

@cf.flow
def interactive_discussion(topic: str):
    agents = [sheldon, leonard, penny, howard, raj]
    
    # Get background information about the topic
    topic_context = get_topic_context(topic)
    
    while True:
        # Let each agent speak
        for agent in agents:
            cf.run(
                "Contribute to the discussion",
                agents=[agent],
                context={
                    "topic": topic,
                    "background_info": topic_context
                },
                interactive=True,
                instructions="Respond to the topic and previous comments in character. "
                           "Use the provided background information to make relevant observations. "
                           "Keep responses 1-2 paragraphs max."
            )
            
        # Get human moderator input
        continue_discussion = cf.run(
            "Ask if the moderator wants to continue the discussion",
            result_type=bool,
            interactive=True
        )
        
        if not continue_discussion:
            break

if __name__ == "__main__":
    topic = input("Enter a topic for discussion: ")
    interactive_discussion(topic=topic)