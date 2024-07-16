from flask import Flask, request, render_template, flash, redirect, url_for
import nltk
from textblob import TextBlob
from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse
import validators
import requests
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

nltk.download('punkt')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def get_video_info(url):
    yt = YouTube(url)
    title = yt.title
    description = yt.description if yt.description else "No description available."
    creator_name = yt.author
    channel_name = "Madawa"  # This should be dynamic if you want to get the actual channel name.
    return title, description, creator_name, channel_name

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript])
        return transcript_text
    except NoTranscriptFound:
        return "Transcript not available for this video."

def summarize_text(text, num_sentences=3):
    sentences = nltk.sent_tokenize(text)
    if len(sentences) > num_sentences:
        summary = ' '.join(sentences[:num_sentences])
    else:
        summary = text
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']

        if validators.url(url):  # Check if URL is valid
            try:
                # Check if it's a YouTube URL
                if 'youtube.com' in url or 'youtu.be' in url:
                    video_id = url.split("v=")[1] if 'youtube.com' in url else url.split("/")[-1]
                    title, description, creator_name, channel_name = get_video_info(url)
                    
                    # Debugging output
                    print(f"Title: {title}")
                    print(f"Description: {description}")
                    print(f"Creator Name: {creator_name}")
                    print(f"Channel Name: {channel_name}")
                    
                    transcript = get_video_transcript(video_id)
                    
                    # Further debug to ensure description is fetched correctly
                    if not description:
                        description = "No description available."
                    # summary = summarize_text(tr, num_sentences=3)
                    # print(f"Summary: {summary}")
                    
                    return render_template('index.html', title=title, description=description, authors=creator_name, youtube_channel=channel_name, youtube_link=url, transcript=transcript)
                
                else:
                    response = requests.get(url)
                    response.raise_for_status()
                    article = Article(url)
                    article.download()
                    article.parse()
                    article.nlp()

                    title = article.title
                    authors = ', '.join(article.authors) if article.authors else get_website_name(url)
                    publish_date = article.publish_date.strftime('%B %d, %Y') if article.publish_date else "N/A"

                    article_text = article.text
                    sentences = article_text.split('.')
                    max_summarized_sentences = 5
                    summary = '.'.join(sentences[:max_summarized_sentences])

                    top_image = article.top_image

                    analysis = TextBlob(article_text)
                    polarity = analysis.sentiment.polarity

                    if polarity > 0:
                        sentiment = 'happy 😊'
                    elif polarity < 0:
                        sentiment = 'sad 😟'
                    else:
                        sentiment = 'neutral 😐'

                    return render_template('index.html', title=title, authors=authors, publish_date=publish_date,
                                           summary=summary, top_image=top_image, sentiment=sentiment)

            except (requests.RequestException, Exception) as e:
                flash('Failed to process the URL: ' + str(e))
                return redirect(url_for('index'))

        else:
            flash('Please enter a valid URL.')
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
