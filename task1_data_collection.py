import requests
import time
import json
import os
from datetime import datetime

# Configuration and Constants
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
MAX_PER_CATEGORY = 25
TOTAL_STORIES_TO_SCAN = 500

# Keyword mapping for categorization
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    """Assigns a category based on keywords found in the title."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    return None

def fetch_trending_stories():
    """Main pipeline to fetch, categorize, and save story data."""
    # Step 1: Get Top Story IDs
    print("Fetching top stories from HackerNews...")
    try:
        response = requests.get(f"{BASE_URL}/top stories.json", headers=HEADERS)
        response.raise_for_status()
        story_ids = response.json()[:TOTAL_STORIES_TO_SCAN]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    collected_data = []
    category_counts = {cat: 0 for cat in CATEGORIES}

    # Step 2: Iterate through categories to fulfill the "sleep per category" requirement
    for category in CATEGORIES:
        print(f"Processing category: {category}...")
        
        for s_id in story_ids:
            # Stop if we already have enough for this category
            if category_counts[category] >= MAX_PER_CATEGORY:
                break
            
            try:
                item_res = requests.get(f"{BASE_URL}/item/{s_id}.json", headers=HEADERS)
                item_res.raise_for_status()
                story = item_res.json()

                if not story or 'title' not in story:
                    continue

                # Check if this story belongs to the current category loop
                assigned_cat = get_category(story['title'])
                
                if assigned_cat == category:
                    # Extract specific fields
                    story_entry = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": assigned_cat,
                        "score": story.get("score"),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    collected_data.append(story_entry)
                    category_counts[category] += 1
            
            except Exception as e:
                print(f"Skipping ID {s_id} due to error: {e}")
                continue

        # Wait 2 seconds between each category loop as per Task 1 requirement
        time.sleep(2)

    # Step 3: Save to JSON
    if not os.path.exists('data'):
        os.makedirs('data')

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, 'w') as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")

if __name__ == "__main__":
    fetch_trending_stories()