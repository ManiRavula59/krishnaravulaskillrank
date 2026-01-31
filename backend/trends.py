import re
from db import cursor

def get_top_hashtags(limit=10):
    cursor.execute("SELECT text FROM posts")
    rows = cursor.fetchall()

    hashtag_count = {}

    for (text,) in rows:
        hashtags = re.findall(r"#\w+", text.lower())
        for tag in hashtags:
            hashtag_count[tag] = hashtag_count.get(tag, 0) + 1

    sorted_tags = sorted(
        hashtag_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_tags[:limit]