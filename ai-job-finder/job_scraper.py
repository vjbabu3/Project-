import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_internshala_jobs(query="data science"):
    """Scrape internships from Internshala"""
    jobs = []
    try:
        encoded_query = urllib.parse.quote(query.replace(" ", "-"))
        url = f"https://internshala.com/internships/{encoded_query}-internship"
        print(f"Scraping Internshala: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Internshala cards can have multiple class variations
        cards = soup.select(".individual_internship, .internship_meta")
        
        for card in cards:
            # Try multiple selectors for title
            title_tag = card.select_one(".heading_4_5, h3, .job-internship-name")
            company_tag = card.select_one(".heading_6, h4, .company-name")
            
            # Find the link within the card
            link_tag = card.find("a", href=True)
            
            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else None
            
            if not title or not company:
                continue
                
            job_url = link_tag['href'] if link_tag else None
            if job_url and not job_url.startswith("http"):
                job_url = f"https://internshala.com{job_url}"
            
            jobs.append({
                "title": title,
                "company": company,
                "source": "Internshala",
                "url": job_url
            })
    except Exception as e:
        print(f"Internshala scraping error: {e}")
    
    return jobs

def get_naukri_jobs(query="data science"):
    """Scrape jobs from Naukri"""
    jobs = []
    try:
        # Naukri is very sensitive. Using a more specialized header.
        naukri_headers = HEADERS.copy()
        naukri_headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.naukri.com/"
        })
        
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.naukri.com/search?k={encoded_query}"
        print(f"Scraping Naukri: {url}")
        
        response = requests.get(url, headers=naukri_headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Naukri uses 'jobTuple' and newer classes like 'cust-job-tuple'
        job_cards = soup.select(".jobTuple, .cust-job-tuple, article")
        
        for card in job_cards:
            title_tag = card.select_one(".title, .jobTitle, h2")
            company_tag = card.select_one(".companyName, .subTitle")
            
            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else None
            
            link_tag = card.find("a", href=True)
            job_url = link_tag.get("href") if link_tag else None
            
            if title and company:
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Naukri",
                    "url": job_url
                })
    except Exception as e:
        print(f"Naukri scraping error: {e}")
    
    return jobs

def get_linkedin_jobs_fallback(query="data science"):
    """Get jobs from LinkedIn alternative (using public search)"""
    jobs = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}"
        print(f"Scraping LinkedIn: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_cards = soup.find_all("div", class_="base-card")
        
        for card in job_cards:
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            link_tag = card.find("a", class_="base-card__full-link", href=True)
            
            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else None
            job_url = link_tag.get("href") if link_tag else None
            
            if title and company:
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "LinkedIn",
                    "url": job_url
                })
    except Exception as e:
        print(f"LinkedIn scraping error: {e}")
    
    return jobs

def get_indeed_jobs(query="data science"):
    """Scrape jobs from Indeed"""
    jobs = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://in.indeed.com/jobs?q={encoded_query}"
        print(f"Scraping Indeed: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_cards = soup.find_all("div", class_="job_seen_beacon")
        
        for card in job_cards:
            title_tag = card.find("h2", class_="jobTitle")
            company_tag = card.find("span", class_="companyName")
            link_tag = card.find("a", href=True)
            
            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else None
            job_url = link_tag.get("href") if link_tag else None
            
            if title and company:
                if job_url and not job_url.startswith("http"):
                    job_url = f"https://in.indeed.com{job_url}"
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Indeed",
                    "url": job_url
                })
    except Exception as e:
        print(f"Indeed scraping error: {e}")
    
    return jobs

def get_remoteok_jobs(query="python"):

    """Fetch jobs from Remote OK JSON API"""
    jobs = []
    try:
        # Remote OK has a public JSON API
        url = "https://remoteok.com/api"
        # Since the API is just 'latest', we filter by query locally
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # First item is a legal notice, skip it
        for item in data[1:]:
            title = item.get("position")
            company = item.get("company")
            job_url = item.get("url")
            tags = item.get("tags", [])
            
            # Simple local filtering
            query_lower = query.lower()
            if any(query_lower in str(tag).lower() for tag in tags) or query_lower in str(title).lower():
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "RemoteOK",
                    "url": job_url
                })
    except Exception as e:
        print(f"Remote OK API error: {e}")
    
    return jobs

def get_shine_jobs(query="python"):
    """Scrape jobs from Shine.com"""
    jobs = []
    try:
        encoded_query = urllib.parse.quote(query.replace(" ", "-"))
        url = f"https://www.shine.com/job-search/{encoded_query}-jobs"
        print(f"Scraping Shine: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Shine uses various classes. Let's try to find title and company 
        # based on structure observed in successful crawls
        cards = soup.select('div[class*="jobCard"], .jobCard_jobCard, [data-testid="job-card"]')
        
        if not cards:
            # Fallback to looking for links that look like jobs
            cards = soup.find_all('h2') + soup.find_all('h3')

        for card in cards:
            title_tag = card.select_one("h2, h3, a") if hasattr(card, 'select_one') else card
            
            # Find company name (usually in a div next to or near the title)
            # Shine often has it in div[class*="jobCard_jobCard_cName"]
            company_tag = None
            if hasattr(card, 'select_one'):
                company_tag = card.select_one('div[class*="cName"], .compName, .company-name')
            
            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else "Check listing"
            
            link_tag = card if card.name == 'a' else card.find("a", href=True)
            job_url = link_tag.get("href") if (link_tag and hasattr(link_tag, 'get')) else None
            
            if job_url and not job_url.startswith("http"):
                job_url = f"https://www.shine.com{job_url}"
                
            if title and "/jobs/" in str(job_url):
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Shine",
                    "url": job_url
                })
    except Exception as e:
        print(f"Shine scraping error: {e}")
    
    return jobs


def get_jobs(query="data science"):
    """
    Aggregate jobs from multiple sources based on query.
    """
    all_jobs = []
    
    scrapers = [
        ("LinkedIn", get_linkedin_jobs_fallback),
        ("Internshala", get_internshala_jobs),
        ("RemoteOK", get_remoteok_jobs),
        ("Shine", get_shine_jobs),
        ("Naukri", get_naukri_jobs),
        ("Indeed", get_indeed_jobs)
    ]
    
    for name, scraper_func in scrapers:
        try:
            print(f"Attempting source: {name}...")
            jobs = scraper_func(query)
            if jobs:
                print(f"✅ {name}: Found {len(jobs)} jobs")
                all_jobs.extend(jobs)
            else:
                print(f"⚠️ {name}: No jobs found or blocked.")
            time.sleep(0.5) 
        except Exception as e:
            print(f"❌ Error in {name} scraper: {e}")
    
    # Final check for total results
    if not all_jobs:
        print("No real jobs found across all platforms. Adding sample entries.")
        all_jobs.append({
            "title": f"Senior {query.title()} Analyst",
            "company": "Dynamic Careers Global (Sample)",
            "source": "System Fallback",
            "url": "https://example.com"
        })
    
    print(f"Done! Aggregated {len(all_jobs)} jobs from all sources.")
    return all_jobs

