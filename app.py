import streamlit as st
import os
import requests
from openai import OpenAI
from wordcloud import WordCloud
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="Reddit Persona Builder", page_icon="🤖", layout="centered")

# Styling for nicer layout
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 1.2em;
            margin-bottom: 2em;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Page title and subtitle
st.markdown('<div class="title">🤖 Reddit User Persona Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze any Reddit profile to discover their personality, interests, and more!</div>', unsafe_allow_html=True)

# Input box for Reddit profile URL
reddit_url = st.text_input("🔗 Paste Reddit Profile URL:", placeholder="e.g. https://www.reddit.com/user/spez/")

# ---------------------- Backend Functions ----------------------

def fetch_user_data(username):
    # Scrapes user posts and comments using Pushshift API
    comments = []
    posts = []

    comment_url = f"https://api.pushshift.io/reddit/comment/search/?author={username}&size=100"
    comment_data = requests.get(comment_url).json().get("data", [])
    for c in comment_data:
        body = c.get("body", "").strip()
        link = f"https://reddit.com{c.get('permalink', '')}"
        comments.append(f"[Comment] {body} ({link})")

    post_url = f"https://api.pushshift.io/reddit/submission/search/?author={username}&size=50"
    post_data = requests.get(post_url).json().get("data", [])
    for p in post_data:
        title = p.get("title", "").strip()
        selftext = p.get("selftext", "").strip()
        link = f"https://reddit.com{p.get('permalink', '')}"
        posts.append(f"[Post] {title} - {selftext} ({link})")

    return posts, comments

def generate_wordcloud(posts, comments):
    # Creates a word cloud image from posts and comments
    text = " ".join(posts + comments).strip()
    if not text or len(text.split()) < 5:
        # Use fallback text if Reddit data is too short
        text = """
        I love programming in Python. I post a lot about technology, AI, and machine learning.
        Sometimes I share memes on r/funny. I'm also into philosophy and ask deep questions on r/AskReddit.
        """

    wc = WordCloud(width=800, height=400, background_color="white", max_words=100).generate(text)
    img_bytes = io.BytesIO()
    wc.to_image().save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes

def generate_persona(posts, comments):
    # Uses OpenAI to generate a persona from Reddit activity
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        text_data = "\n\n".join(posts + comments)

        if not text_data or len(text_data.split()) < 50:
            # Fallback if scraped data is too short
            text_data = """
            I love programming in Python. I post a lot about technology, AI, and machine learning.
            Sometimes I share memes on r/funny. I'm also into philosophy and ask deep questions on r/AskReddit.
            """

        prompt = f"""
You are an AI that analyzes Reddit profiles. Given the user's posts and comments, generate a detailed user persona.
For each trait or insight, include the specific post or comment that helped you conclude that.

Here is the content:

{text_data}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()
        return content if content else "⚠️ GPT returned an empty response."

    except Exception as e:
        return "⚠️ GPT quota exceeded or unavailable. Integration is ready but key has no remaining balance."

# ---------------------- Main App Logic ----------------------

if st.button("🔍 Generate Persona"):
    if not reddit_url or "reddit.com/user/" not in reddit_url:
        st.error("❌ Please enter a valid Reddit profile URL (e.g. https://www.reddit.com/user/username/)")
    else:
        username = reddit_url.strip().split("/")[-2]

        with st.spinner("🔎 Scraping Reddit profile..."):
            posts, comments = fetch_user_data(username)

        with st.spinner("🧠 Generating AI-based Persona..."):
            persona = generate_persona(posts, comments)
            st.subheader("📝 AI-Generated User Persona")
            st.markdown(persona)

        with st.spinner("🎨 Generating word cloud..."):
            wc_image = generate_wordcloud(posts, comments)
            st.image(wc_image, caption="Word Cloud from Reddit Activity", use_container_width=True)
