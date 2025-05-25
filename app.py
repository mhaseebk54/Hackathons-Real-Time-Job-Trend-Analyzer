from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from scraper import scrape_indeed, scrape_linkedin, analyze_jobs
import schedule
import time
import threading
import os

app = Flask(__name__)

# Ensure directories exist
os.makedirs("static/plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

def run_scraper():
    """Run scraping and update data"""
    print("🔄 Running scraper...")
    indeed_jobs = scrape_indeed(max_pages=2)
    linkedin_jobs = scrape_linkedin(max_pages=2)
    all_jobs = indeed_jobs + linkedin_jobs
    
    # Save data
    df = pd.DataFrame(all_jobs)
    df.to_csv("data/jobs_data.csv", index=False)
    
    # Generate plots
    analysis = analyze_jobs(all_jobs)
    plt.figure(figsize=(10, 5))
    analysis["posting_trends"].plot(title="Job Posting Trends")
    plt.savefig("static/plots/trends.png")
    plt.close()
    
    return analysis

# Initial data load
current_data = run_scraper()

# Scheduled scraping every 60 minutes
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every(60).minutes.do(lambda: globals().update({"current_data": run_scraper()}))
threading.Thread(target=scheduler, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        global current_data
        current_data = run_scraper()
    
    return render_template(
        "dashboard.html",
        titles=current_data["top_titles"],
        skills=current_data["top_skills"],
        cities=current_data["top_cities"]
    )

if __name__ == "__main__":
    app.run(debug=True)