import sqlite3

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("socialmedia.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- POSTS TABLE ----------------
# Stores raw social media posts
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    sentiment TEXT,
    hashtag TEXT,
    created_at TEXT
)
""")

# ---------------- TRENDS TABLE ----------------
# Stores trending hashtags
cursor.execute("""
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hashtag TEXT,
    count INTEGER
)
""")

# ---------------- TIME SERIES TABLE ----------------
# Used for posts-over-time graph
cursor.execute("""
CREATE TABLE IF NOT EXISTS time_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hour TEXT,
    count INTEGER
)
""")

conn.commit()

# ---------------- HELPER FUNCTIONS ----------------

def insert_post(text, sentiment, hashtag, created_at):
    cursor.execute(
        "INSERT INTO posts (text, sentiment, hashtag, created_at) VALUES (?, ?, ?, ?)",
        (text, sentiment, hashtag, created_at)
    )
    conn.commit()


def get_stats():
    cursor.execute("SELECT COUNT(*) FROM posts")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts WHERE sentiment='positive'")
    positive = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts WHERE sentiment='neutral'")
    neutral = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts WHERE sentiment='negative'")
    negative = cursor.fetchone()[0]

    return {
        "total_posts": total,
        "positive": positive,
        "neutral": neutral,
        "negative": negative
    }


def get_trends(limit=10):
    cursor.execute("""
        SELECT hashtag, COUNT(*) as cnt
        FROM posts
        WHERE hashtag IS NOT NULL
        GROUP BY hashtag
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()


def get_time_series():
    cursor.execute("""
        SELECT created_at, COUNT(*) 
        FROM posts
        GROUP BY created_at
        ORDER BY created_at
    """)
    return cursor.fetchall()