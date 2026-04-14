import pandas as pd
import numpy as np
import os

# --- Task 1: Load and Explore ---

# Load the CSV (Ensure the path is correct relative to your script)
file_path = 'data/trends_clean.csv'
df = pd.read_csv(file_path)

# Print basic info
print(f"Loaded data: {df.shape}")
print("First 5 rows:")
print(df.head())

# Calculate averages using Pandas
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()
print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

print("\n--- NumPy Stats ---")

# --- Task 2: Basic Analysis with NumPy ---

# Convert columns to NumPy arrays for calculation
scores = df['score'].values
comments = df['num_comments'].values

# Calculate stats using np.mean(), np.median(), np.std(), np.max(), np.min()
mean_val = np.mean(scores)
median_val = np.median(scores)
std_val = np.std(scores)
max_val = np.max(scores)
min_val = np.min(scores)

print(f"Mean score   : {mean_val:,.0f}")
print(f"Median score : {median_val:,.0f}")
print(f"Std deviation: {std_val:,.0f}")
print(f"Max score    : {max_val:,.0f}")
print(f"Min score    : {min_val:,.0f}")

# Finding the category with most stories
# Tip: value_counts() is great, but ensure you mention the top one
top_category = df['category'].value_counts().idxmax()
cat_count = df['category'].value_counts().max()
print(f"Most stories in: {top_category} ({cat_count} stories)")

# Find most commented story
# Tip: use df.loc[df['num_comments'].idxmax()] to get the full row
top_story_row = df.loc[df['num_comments'].idxmax()]
print(f"Most commented story: \"{top_story_row['title']}\" — {top_story_row['num_comments']} comments")

# --- Task 3: Add New Columns ---

# Formula: engagement = num_comments / (score + 1)
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# Formula: is_popular = True if score > avg_score
df['is_popular'] = df['score'] > avg_score

# --- Task 4: Save the Result ---

output_path = 'data/trends_analysed.csv'
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")