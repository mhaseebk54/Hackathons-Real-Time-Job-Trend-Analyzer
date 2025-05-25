import streamlit as st
from scraper import scrape_indeed, scrape_linkedin, analyze_jobs
import pandas as pd

# Set up the page
st.title("Job Scraper Dashboard")
st.write("This app shows job listings from Indeed and LinkedIn")

# Add a button to run the scraper
if st.button("Get Job Listings"):
    st.write("Scraping jobs... Please wait...")
    
    # Run your existing scrapers
    indeed_jobs = scrape_indeed(max_pages=1)
    linkedin_jobs = scrape_linkedin(max_pages=1)
    all_jobs = indeed_jobs + linkedin_jobs
    
    # Show basic info
    st.success(f"Found {len(all_jobs)} jobs!")
    
    # Show the jobs in a table
    st.subheader("All Job Listings")
    st.dataframe(pd.DataFrame(all_jobs))
    
    # Show top job titles
    st.subheader("Top Job Titles")
    title_counts = pd.DataFrame(all_jobs)["Title"].value_counts().head(5)
    st.bar_chart(title_counts)
    
    # Show top locations
    st.subheader("Top Locations")
    location_counts = pd.DataFrame(all_jobs)["Location"].value_counts().head(5)
    st.bar_chart(location_counts)
    
    # Show job sources
    st.subheader("Job Sources")
    source_counts = pd.DataFrame(all_jobs)["Source"].value_counts()
    st.bar_chart(source_counts)