import requests
import time
import pandas as pd

# Editable parameters
subreddits = ["zelda"]
keywords = ["beedle"]
limit = 100  # posts per subreddit

def contains_keyword(text, keywords):
    return any(kw.lower() in text.lower() for kw in keywords)

def fetch_posts(subreddit, limit=100):
    url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={limit}&sort=desc"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch from {subreddit}")
        return []
    return response.json().get("data", [])

def main():
    results = []
    for sub in subreddits:
        print(f"Searching in r/{sub}")
        posts = fetch_posts(sub, limit)
        for post in posts:
            title = post.get("title", "")
            selftext = post.get("selftext", "")
            if contains_keyword(title + " " + selftext, keywords):
                results.append({
                    "subreddit": sub,
                    "title": title,
                    "author": post.get("author"),
                    "url": f"https://www.reddit.com{post.get('permalink')}",
                    "created_utc": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post["created_utc"]))
                })

    df = pd.DataFrame(results)
    df.to_csv("keyword_matches.csv", index=False)
    print(f"\nFound {len(results)} matching posts. Saved to keyword_matches.csv")

if __name__ == "__main__":
    main()
