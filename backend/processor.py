import csv
import re
from db import cursor, conn
from transformers import pipeline

# dataset path
DATA_PATH = "/Users/lokeshwarikonala/Desktop/socialmediaengine/data/training.1600000.processed.noemoticon.csv"

# load HuggingFace sentiment model (once at startup)
sentiment_model = pipeline("sentiment-analysis")

def extract_hashtags(text):
    return re.findall(r"#\w+", text.lower())

def analyze_sentiment(text):
    try:
        result = sentiment_model(text[:512])[0]  # limit long text
        label = result["label"]

        if label == "POSITIVE":
            return "positive"
        else:
            return "negative"

    except:
        # fallback safety
        return "neutral"

def process_posts():
    cursor.execute("DELETE FROM posts")
    cursor.execute("DELETE FROM trends")
    conn.commit()

    total = 0
    hashtag_counts = {}

    with open(DATA_PATH, encoding="latin-1") as f:
        reader = csv.reader(f)

        for row in reader:
            text = row[5]
            created_at = row[2]

            sentiment = analyze_sentiment(text)

            cursor.execute(
                "INSERT INTO posts(text, sentiment, created_at) VALUES (?, ?, ?)",
                (text, sentiment, created_at),
            )

            hashtags = extract_hashtags(text)
            for tag in hashtags:
                hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1

            total += 1

            # hackathon requirement
            if total >= 500000:
                break

            if total % 1000 == 0:
                print("Processed:", total)

    for tag, count in hashtag_counts.items():
        cursor.execute(
            "INSERT INTO trends(hashtag, count) VALUES (?, ?)",
            (tag, count),
        )

    conn.commit()

    return {"total_posts": total}