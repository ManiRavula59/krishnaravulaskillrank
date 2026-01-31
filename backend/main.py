from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from processor import process_posts
from insights import generate_insights, ask_ai
from trends import get_top_hashtags
from db import cursor, get_stats

# ---------------- CREATE APP ----------------
app = FastAPI(title="Real-Time Social Media Insight Engine")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- AI QUESTION ENDPOINT ----------------
@app.post("/ask")
def ask(question: str = Body(...)):
    return {"answer": ask_ai(question)}

# ---------------- PROCESS DATA ----------------
@app.get("/process")
def process():
    summary = process_posts()
    return {
        "message": f"Analyzed {summary['total_posts']} posts",
        "summary": summary
    }

# ---------------- STATS ----------------
@app.get("/stats")
def stats():
    return get_stats()

# ---------------- TRENDS ----------------
@app.get("/trends")
def trends():
    return get_top_hashtags()

# ---------------- TIME SERIES ----------------
@app.get("/timeseries")
def get_timeseries():
    cursor.execute("""
        SELECT created_at, COUNT(*) 
        FROM posts 
        GROUP BY created_at
        ORDER BY created_at
    """)
    return cursor.fetchall()

# ---------------- LLM INSIGHTS ----------------
@app.get("/insights")
def insights():
    return {"insights": generate_insights()}