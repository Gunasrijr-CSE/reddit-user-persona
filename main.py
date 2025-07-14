import praw
import os
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load keys from .env
load_dotenv()

# Setup Reddit API client    #changed to read only
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=None,
    user_agent=os.getenv("REDDIT_USER_AGENT")
)
reddit.read_only = True




# Function to fetch posts and comments
import requests

def fetch_user_data(username):
    comments = []
    posts = []

    # Fetch comments
    comment_url = f"https://api.pushshift.io/reddit/comment/search/?author={username}&size=100"
    comment_data = requests.get(comment_url).json().get("data", [])
    for c in comment_data:
        body = c.get("body", "").strip()
        link = f"https://reddit.com{c.get('permalink', '')}"
        comments.append(f"[Comment] {body} ({link})")

    # Fetch submissions
    post_url = f"https://api.pushshift.io/reddit/submission/search/?author={username}&size=50"
    post_data = requests.get(post_url).json().get("data", [])
    for p in post_data:
        title = p.get("title", "").strip()
        selftext = p.get("selftext", "").strip()
        link = f"https://reddit.com{p.get('permalink', '')}"
        posts.append(f"[Post] {title} - {selftext} ({link})")

    return posts, comments


# Function to create a word cloud
def generate_wordcloud(username, posts, comments):
    text = " ".join(posts + comments).strip()

    if not text or len(text.split()) < 5:
        print("⚠️ No real content — using demo text for word cloud.")
        text = """
        I love programming in Python. I post a lot about technology, AI, and machine learning.
        Sometimes I share memes on r/funny. I'm also into philosophy and ask deep questions on r/AskReddit.
        """

    try:
        wc = WordCloud(width=800, height=400, background_color="white", max_words=100).generate(text)
        image_path = f"{username}_wordcloud.png"
        wc.to_file(image_path)
        print(f"✅ Word cloud saved as {image_path}")
    except Exception as e:
        print(f"❌ Word cloud generation failed: {e}")



import openai

def generate_persona(username, posts, comments):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    text_data = "\n\n".join(posts + comments)
    
    if not text_data or len(text_data.split()) < 50:
        print("⚠️ Not enough real data — using demo text for persona.")
        text_data = """
        I love programming in Python. I post a lot about technology, AI, and machine learning.
        Sometimes I share memes on r/funny. I'm also into philosophy and ask deep questions on r/AskReddit.
        """


    prompt = f"""
You are an AI that analyzes Reddit profiles. Given the user's posts and comments, generate a detailed user persona. 
For each trait or insight, also include the specific post or comment that helped you conclude that.

Example:
- Interest: Technology (from: "I just built my own PC..." - reddit.com/xyz)
- Personality: Curious (from: "Why do people still use..." - reddit.com/abc)

Here is the content:

{text_data}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        persona = response['choices'][0]['message']['content']
        
        with open(f"{username}_persona.txt", "w", encoding="utf-8") as f:
            f.write(persona)

        print(f"✅ Persona generated and saved to {username}_persona.txt")
    except Exception as e:
        print("❌ Error generating persona:", e)




# Main program
if __name__ == "__main__":
    url = input("Enter Reddit profile URL: ").strip()
    username = url.split("/")[-2]
    posts, comments = fetch_user_data(username)

    # Save posts and comments to text file
    with open(f"{username}_data.txt", "w", encoding="utf-8") as f:
        f.write("---- POSTS ----\n" + "\n\n".join(posts))
        f.write("\n\n---- COMMENTS ----\n" + "\n\n".join(comments))

    print(f"✅ Data saved to {username}_data.txt")

    # Generate word cloud
    generate_wordcloud(username, posts, comments)
