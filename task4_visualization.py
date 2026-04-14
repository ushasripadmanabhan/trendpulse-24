import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Task 1: Setup ---
# Load the data from Task 3
df = pd.read_csv('data/trends_analysed.csv')

# Create output directory if it doesn't exist
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# --- Task 2: Chart 1 - Top 10 Stories (Horizontal Bar) ---
plt.figure(figsize=(10, 6))

# Sort and take top 10
top_10 = df.sort_values(by='score', ascending=False).head(10)

# Shorten long titles using a lambda function
short_titles = top_10['title'].apply(lambda x: x[:47] + "..." if len(x) > 50 else x)

plt.barh(short_titles, top_10['score'], color='skyblue')
plt.xlabel('Score')
plt.title('Top 10 Stories by Score')
plt.gca().invert_yaxis()  # Put the highest score at the top
plt.tight_layout()
plt.savefig('outputs/chart1_top_stories.png')
plt.close() # Close to free up memory

# --- Task 3: Chart 2 - Stories per Category (Bar) ---
plt.figure(figsize=(8, 6))
cat_counts = df['category'].value_counts()

# Plot using a variety of colors
cat_counts.plot(kind='bar', color=['tomato', 'olivedrab', 'gold', 'orchid', 'teal'])
plt.title('Number of Stories per Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/chart2_categories.png')
plt.close()

# --- Task 4: Chart 3 - Score vs Comments (Scatter) ---
plt.figure(figsize=(8, 6))

# Separate popular and non-popular for different colors
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

plt.scatter(not_popular['score'], not_popular['num_comments'], color='gray', label='Standard', alpha=0.5)
plt.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', edgecolors='red')

plt.title('Engagement: Score vs Comments')
plt.xlabel('Score')
plt.ylabel('Number of Comments')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/chart3_scatter.png')
plt.close()

# --- Bonus: Dashboard ---
# We create a large figure and add the plots back in
fig, axs = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('TrendPulse Dashboard', fontsize=20)

# Dashboard - Subplot 1: Top Stories
axs[0, 0].barh(short_titles, top_10['score'], color='skyblue')
axs[0, 0].set_title('Top 10 Stories')
axs[0, 0].invert_yaxis()

# Dashboard - Subplot 2: Categories
axs[0, 1].bar(cat_counts.index, cat_counts.values, color='teal')
axs[0, 1].set_title('Stories per Category')

# Dashboard - Subplot 3: Scatter
axs[1, 0].scatter(df['score'], df['num_comments'], c=df['is_popular'].map({True: 'orange', False: 'blue'}))
axs[1, 0].set_title('Score vs Comments')

# Remove the empty 4th subplot
fig.delaxes(axs[1, 1])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('outputs/dashboard.png')
print("All charts and dashboard saved in outputs/ folder.")