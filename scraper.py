import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter


def scrape_indeed(query="Python Developer", location="Pakistan", max_pages=2):
    """Scrapes job listings from Indeed"""
    base_url = "https://pk.indeed.com/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    jobs = []

    for page in range(max_pages):
        params = {
            "q": query,
            "l": location,
            "start": page * 10
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        for job in soup.find_all("div", class_="job_seen_beacon"):
            title_tag = job.find("h2", class_="jobTitle")
            company_tag = job.find("span", class_="companyName")
            location_tag = job.find("div", class_="companyLocation")
            date_tag = job.find("span", class_="date")
            
            jobs.append({
                "Title": title_tag.text.strip() if title_tag else None,
                "Company": company_tag.text.strip() if company_tag else None,
                "Location": location_tag.text.strip() if location_tag else None,
                "Date Posted": date_tag.text.strip() if date_tag else None,
                "Source": "Indeed"
            })

    return jobs

def scrape_linkedin(query="Python Developer", location="USA", max_pages=2):
    
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    jobs = []
    
    for page in range(max_pages):
        params = {
            "keywords": query,
            "location": location,
            "start": page * 25
        }
        
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for job in soup.find_all("li"):
            title = job.find("h3").text.strip()
            company = job.find("h4").text.strip()
            location = job.find("span", class_="job-search-card__location").text.strip()
            date = job.find("time")["datetime"] if job.find("time") else "N/A"
            
            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Date Posted": date,
                "Source": "LinkedIn"
            })
    
    return jobs

def analyze_jobs(jobs):
    df = pd.DataFrame(jobs)
    
   
    top_titles = Counter(df["Title"]).most_common(5)
    print("\n🔥 Top Job Titles:")
    for title, count in top_titles:
        print(f"- {title} ({count} jobs)")
    
    top_cities = Counter(df["Location"]).most_common(5)
    print("\n📍 Top Hiring Cities:")
    for city, count in top_cities:
        print(f"- {city} ({count} jobs)")
    
   
    df.to_csv("data/jobs_data.csv", index=False)
    print("\n✅ Data saved to 'data/jobs_data.csv'")

if __name__ == "__main__":
    print("🚀 Scraping Indeed...")
    indeed_jobs = scrape_indeed(max_pages=1)
    
    print("🚀 Scraping LinkedIn...")
    linkedin_jobs = scrape_linkedin(max_pages=1)
    
    all_jobs = indeed_jobs + linkedin_jobs
    analyze_jobs(all_jobs)