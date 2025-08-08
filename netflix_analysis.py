# netflix_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Step 1: Load the dataset
try:
    df = pd.read_csv('netflix1.csv')
    print("✅ Dataset loaded successfully!")
    print(df.head())
except FileNotFoundError:
    print("❌ Error: File 'netflix1.csv' not found. Make sure it's in the project folder.")
    exit()

# Step 2: Drop duplicates
df.drop_duplicates(inplace=True)

# Step 3: Drop rows with nulls in important columns (only if the column exists)
required_columns = ['director', 'cast', 'country']
existing_columns = [col for col in required_columns if col in df.columns]
if existing_columns:
    df.dropna(subset=existing_columns, inplace=True)

# Step 4: Convert 'date_added' to datetime (if it exists)
if 'date_added' in df.columns:
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
else:
    print("⚠️ Warning: 'date_added' column not found. Skipping date analysis.")

# Step 5: Content Type Distribution (Movies vs TV Shows)
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=df, palette='Set2')
plt.title("Content Types: Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig('type_distribution.png')
plt.clf()

# Step 6: Top 10 Genres
if 'listed_in' in df.columns:
    df['genres'] = df['listed_in'].apply(lambda x: x.split(', '))
    all_genres = sum(df['genres'], [])
    genre_counts = pd.Series(all_genres).value_counts().head(10)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='Set3')
    plt.title("Top 10 Genres on Netflix")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.savefig('top_genres.png')
    plt.clf()
else:
    print("⚠️ Warning: 'listed_in' column not found. Skipping genre analysis.")

# Step 7: Word Cloud of Movie Titles
if 'title' in df.columns and 'type' in df.columns:
    movie_titles = df[df['type'] == 'Movie']['title']
    text = ' '.join(movie_titles.dropna())
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title("Word Cloud of Movie Titles")
        plt.tight_layout()
        plt.savefig('wordcloud.png')
        plt.clf()
    else:
        print("⚠️ No movie titles found to generate word cloud.")
else:
    print("⚠️ Required columns missing for word cloud generation.")

# Final message
print("✅ Analysis complete. Visuals saved as:")
print("- type_distribution.png")
print("- top_genres.png")
print("- wordcloud.png")
