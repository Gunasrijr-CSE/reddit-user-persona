# Reddit User Persona Generator 

A AI project that analyzes Reddit users based on their posts and comments to build a personality profile using OpenAI GPT and visualize their activity with a word cloud.

## Features

- 🔍 Scrapes recent Reddit posts and comments using Pushshift API
- 🧠 Generates an AI-powered user persona via OpenAI GPT
- 🎨 Creates a word cloud from user activity
- 💡 Built using Python, Streamlit, and OpenAI API

---

## 🖥 Demo Preview

| Persona Output                         | Word Cloud                            |
|----------------------------------------|----------------------------------------|
| ![Persona](screenshots/ui.png)         | ![WordCloud](screenshots/wordcloud.png) |

---

## How to Run Locally

 1️⃣ Clone the repo

git clone https://github.com/Gunasrijr-CSE/reddit-user-persona.git
cd reddit-user-persona

2️⃣ Install requirements

pip install -r requirements.txt

3️⃣ Add your OpenAI API key
Create a .env file in the root folder and add:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

4️⃣ Run the app

streamlit run app.py
Paste a Reddit user URL like:
https://www.reddit.com/user/Hungry-Move-6603/

## Tech Stack
Python

Streamlit

OpenAI API (gpt-3.5-turbo)

Pushshift API (for Reddit data)

WordCloud & Pillow

## Author
Made with 💻 by Gunasri J R
For the BeyondChats Generative AI Internship Challenge.






