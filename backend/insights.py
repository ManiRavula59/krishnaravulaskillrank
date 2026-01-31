import os
from google import genai
from db import cursor

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- DATABASE INSIGHTS ----------------
def generate_insights():
    try:
        cursor.execute("""
            SELECT sentiment, COUNT(*)
            FROM posts
            GROUP BY sentiment
        """)
        data = cursor.fetchall()

        prompt = f"""
        You are a social media analyst.

        Sentiment breakdown from 500K posts:
        {data}

        Generate 3 business insights:
        - Title
        - Explanation
        - Risk level
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Insight generation failed: {str(e)}"


# ---------------- FRONTEND AI QUESTION ----------------
def ask_ai(question: str):
    try:
        # Pull trending data to help AI answer
        cursor.execute("""
            SELECT hashtag, count
            FROM trends
            ORDER BY count DESC
            LIMIT 10
        """)
        trends = cursor.fetchall()

        prompt = f"""
        You are an AI social media analyst.

        Trending hashtags:
        {trends}

        User question:
        {question}

        Answer based on the dataset above.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI query failed: {str(e)}"