# 📰🔍 Web & YouTube Analyzer with Flask

This Flask web app allows users to input either a **YouTube video link** or a **news/article URL**. It then intelligently analyzes the content to provide:

- 📃 **Summaries** of articles and video transcripts  
- 😊 **Sentiment analysis** for articles  
- 🎬 **YouTube video metadata** (title, description, creator, transcript)  
- 🧠 **Smart NLP** features powered by `nltk`, `TextBlob`, `newspaper3k`, and `YouTube Transcript API`

---

## 🚀 Features

- ✅ Accepts **any valid URL** – smartly distinguishes between YouTube and web articles.
- 📄 **Web Article Processing:**
  - Extracts title, publish date, authors, top image.
  - Summarizes content using sentence splitting.
  - Analyzes sentiment (happy, sad, or neutral).
- 📺 **YouTube Video Processing:**
  - Fetches title, description, and creator name.
  - Extracts and displays video transcript (if available).
- 🧠 Uses **TextBlob** and **NLTK** for sentiment and NLP.
- 🧪 Clean, modular backend built with **Flask**.

---
## 🧠 About

This application allows users to input a URL (either from a web article or a YouTube video) and get a summary, sentiment analysis, and other useful details.

Key Features:
- **Article Parsing**: Extracts the title, authors, and text from web articles.
- **YouTube Parsing**: Fetches video title, description, and transcript (if available).
- **Text Summarization**: Provides a short summary of the article or transcript.
- **Sentiment Analysis**: Analyzes the text's sentiment (positive, negative, or neutral).

## 🖼️ App Screenshot

> _Example: Analyzing a YouTube video and a blog article using the app._

---

## 🧩 Workflow

```mermaid
graph TD;
    A[User Submits URL] --> B{Is it YouTube?}
    B -- Yes --> C[Fetch Metadata with pytube]
    C --> D[Get Transcript with YouTubeTranscriptAPI]
    D --> E[Render Title, Description, Creator, Transcript]

    B -- No --> F[Scrape Article with newspaper3k]
    F --> G[Summarize & Sentiment Analysis with TextBlob]
    G --> H[Render Title, Summary, Sentiment, Author, Image]
