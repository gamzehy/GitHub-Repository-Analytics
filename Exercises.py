import json
import pandas as pd
import streamlit as st
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import pytest

with open("repos.json", "r") as f:
    data = json.load(f)


# Convert JSON to a DataFrame for easier manipulation
repos_df = pd.json_normalize(data)

def test_data_integrity():
    # Check notnull values in key columns
    assert repos_df['name'].notnull().all(), "All repositories should have names"
    assert repos_df['created_at'].notnull().all(), "All repositories should have creation dates"
    assert repos_df['stargazers_count'].notnull().all(), "All repositories should have a stargazer count"

# Quick Data Overview
(repos_df.head())
(repos_df.info())
type(repos_df)

# Creating New Column
repos_df['created_year'] = pd.to_datetime(repos_df['created_at']).dt.year.astype(int)

# Page Naming
st.title("GitHub Repository Analytics")
st.sidebar.header("Filter for Repository Owner")

# Filter by Owner
owner_filter = st.sidebar.selectbox("Select Repository Owner", repos_df['owner.login'].unique())
filtered_df = repos_df[repos_df['owner.login'] == owner_filter]

# Calculate count of Repos - KPIs
yearly_repo_count = filtered_df.groupby('created_year').size()

# Visualize Repositories Created by Year
st.subheader("Repositories Created by Year")
fig, ax = plt.subplots()
yearly_repo_count.plot(kind='bar', ax=ax,color="blue")
max_y = int(yearly_repo_count.max())
ax.set_yticks(range(0, max_y + 1, 1))
ax.set_xlabel("Year")
ax.set_ylabel("Repository Count")
st.pyplot(fig)

filtered_df['created_year']=filtered_df['created_year'].astype(str)

# Creating Table for Visibility - Double Check
st.subheader("Repository Table")
st.dataframe(filtered_df[['name', 'created_year', 'updated_at',  'stargazers_count', 'watchers_count', 'description']])

# Q1 - Most Famous Repo
most_starred_repo = filtered_df.loc[filtered_df['stargazers_count'].idxmax()]
st.write("Most famous repository:", most_starred_repo['name'],  " with stars:", most_starred_repo['stargazers_count'])

# Q2 - Recently Updated Repo
most_recent_repo = filtered_df.loc[filtered_df['updated_at'].idxmax()]
st.write("Most recently updated repository:", most_recent_repo['name'], " last updated on:", most_recent_repo['updated_at'])

# Q3 - Nb of Desc & Most Common Word
repos_with_desc = filtered_df[filtered_df['description'].notnull()]
description_words = ' '.join(repos_with_desc['description']).split()
most_common_word = Counter(description_words).most_common(1)[0]
st.write(f"Repositories with a description: {len(repos_with_desc)}")
no_description_df = filtered_df[filtered_df['description'].isnull()]
num_no_desc = len(no_description_df)
st.write(f"Repositories without a description: {num_no_desc}")
st.write(f"The word '{most_common_word[0]}' appears most frequently across descriptions, with a count of {most_common_word[1]}.")


# Test for Most Starred Repository - Validation Check
def test_most_starred_repo():
    max_stars = filtered_df['stargazers_count'].max()
    assert most_starred_repo['stargazers_count'] == max_stars, "Most starred repository calculation error"

# Test for Most Recent Update in Repositories - Validation Check
def test_most_recent_repo():
    latest_update = filtered_df['updated_at'].max()
    assert most_recent_repo['updated_at'] == latest_update, "Most recent repository update calculation error"

    pytest.main()

