import pandas as pd
import glob
import os

# --- 1 — Load the JSON File ---

# Locate the file in the data folder (handles the YYYYMMDD format)
# Note: glob.glob helps find files with a pattern if you don't know the exact date
files = glob.glob('data/trends_*.json')
if not files:
    print("Error: No JSON file found in the data/ folder.")
    exit()

json_path = files[0] # Take the first matching file
df = pd.read_json(json_path)

print(f"Loaded {len(df)} stories from {json_path}")

# --- 2 — Clean the Data ---

# A. Remove Duplicates based on post_id
df.drop_duplicates(subset=['post_id'], inplace=True)
print(f"After removing duplicates: {len(df)}")

# B. Remove Missing Values (dropna)
# We focus on the critical columns required by the task
df.dropna(subset=['post_id', 'title', 'score'], inplace=True)
print(f"After removing nulls: {len(df)}")

# C. Fix Data Types
# Ensure score and num_comments are integers
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].astype(int)

# D. Filter Low Quality
# Keep only stories where score >= 5
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")

# E. Clean Whitespace
# Use .str.strip() to clean the title column
df['title'] = df['title'].str.strip()

# --- 3 — Save as CSV ---

output_path = 'data/trends_clean.csv'
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")

# F. Summary Print
print("\nStories per category:")
# Use value_counts() to get the distribution per category
print(df['category'].value_counts())