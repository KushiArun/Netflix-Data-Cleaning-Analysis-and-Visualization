# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(
    page_title="Netflix Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎯 Sidebar Title
st.sidebar.title("🎬 Netflix Data Explorer")
st.sidebar.markdown("Use the filters below to explore the dataset:")

# 📥 Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("netflix1.csv")
    df.drop_duplicates(inplace=True)
    
    # Clean conditionally
    for col in ['director', 'cast', 'country']:
        if col in df.columns:
            df.dropna(subset=[col], inplace=True)

    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df.dropna(subset=['date_added'], inplace=True)
        df['year_added'] = df['date_added'].dt.year
        df['month_added'] = df['date_added'].dt.month
    
    if 'listed_in' in df.columns:
        df['genres'] = df['listed_in'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    
    return df

df = load_data()

# Sidebar filters
types = st.sidebar.multiselect("Select Content Type", df['type'].unique(), default=df['type'].unique())
year_range = st.sidebar.slider("Select Release Year Range", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2021))

filtered_df = df[
    (df['type'].isin(types)) &
    (df['release_year'].between(year_range[0], year_range[1]))
]

# 🎨 Styling
st.title("📊 Netflix Content Dashboard")
st.markdown("A beautifully interactive dashboard to explore Netflix shows and movies dataset.")

st.markdown("---")

# 📺 Content Type Distribution
st.subheader("📺 Distribution of Content Types")
col1, col2 = st.columns(2)

with col1:
    type_count = filtered_df['type'].value_counts()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=type_count.index, y=type_count.values, palette='Set2', ax=ax1)
    ax1.set_title("Movies vs TV Shows")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

with col2:
    st.metric(label="Total Titles", value=len(filtered_df))
    st.metric(label="Movies", value=type_count.get("Movie", 0))
    st.metric(label="TV Shows", value=type_count.get("TV Show", 0))

# 🎭 Top Genres
st.subheader("🎭 Top 10 Genres")

all_genres = sum(filtered_df['genres'], [])
genre_counts = pd.Series(all_genres).value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='Set3', ax=ax2)
ax2.set_xlabel("Count")
ax2.set_ylabel("Genres")
st.pyplot(fig2)

# 🧠 Word Cloud of Movie Titles
st.subheader("🧠 Word Cloud of Movie Titles")
movies = filtered_df[filtered_df['type'] == 'Movie']['title'].dropna()
if not movies.empty:
    wc = WordCloud(width=800, height=400, background_color='black').generate(' '.join(movies))
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.imshow(wc, interpolation='bilinear')
    ax3.axis('off')
    st.pyplot(fig3)
else:
    st.warning("No movie titles available for word cloud with current filters.")

# 📈 Content by Year
if 'year_added' in filtered_df.columns:
    st.subheader("📆 Content Added Over Years")

    movies_by_year = filtered_df[filtered_df['type'] == 'Movie']['year_added'].value_counts().sort_index()
    shows_by_year = filtered_df[filtered_df['type'] == 'TV Show']['year_added'].value_counts().sort_index()

    fig4, ax4 = plt.subplots()
    ax4.plot(movies_by_year.index, movies_by_year.values, marker='o', label='Movies', color='skyblue')
    ax4.plot(shows_by_year.index, shows_by_year.values, marker='o', label='TV Shows', color='salmon')
    ax4.set_xlabel("Year")
    ax4.set_ylabel("Number of Titles Added")
    ax4.set_title("Netflix Content Added Over Time")
    ax4.legend()
    ax4.grid(True)
    st.pyplot(fig4)

# 📊 Rating Distribution
if 'rating' in filtered_df.columns:
    st.subheader("⭐ Ratings Distribution")
    rating_counts = filtered_df['rating'].value_counts().head(10)
    fig5, ax5 = plt.subplots()
    sns.barplot(x=rating_counts.values, y=rating_counts.index, palette='coolwarm', ax=ax5)
    ax5.set_title("Top 10 Ratings")
    st.pyplot(fig5)

# 📍 Footer
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) | Dataset: [Netflix Shows on Kaggle](https://www.kaggle.com/shivamb/netflix-shows)")

