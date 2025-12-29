import requests
from bs4 import BeautifulSoup
from .models import JobPosting
from users.models import Company
import time
from urllib.parse import urljoin

def scrape_job_details(job_url):
    """Scrape detailed job description from the job posting page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    try:
        response = requests.get(job_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Assuming the job description is within a div with class 'job-full-desc'
        desc_div = soup.find("li", class_="job-description")
        description_html = str(desc_div) if desc_div else None
        
        # extract direct application link if available
        application_url = None
        method_header = soup.find("h2", id="application-method")

        if method_header:
            container = method_header.find_next_sibling("div")
            if container:
                a_tag = container.find("a")
                if a_tag and a_tag.has_attr('href'):
                    raw_link = a_tag['href']
                    application_url = urljoin(job_url, raw_link)
        return description_html, application_url

    except Exception as e:
        print(f"Error fetching job details from {job_url}: {e}")
        return "Error fetching job details."


def scrape_myjobmag():
    # Target URL
    base_url = "https://www.myjobmag.co.ke" 
    target_url = f"{base_url}/jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    try:
        print(f"Fetching {target_url}...")
        response = requests.get(target_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        job_list = soup.find("ul", class_="job-list")
        
        if not job_list:
            print("Could not find job list container. Structure might have changed.")
            return

        # Find all job items
        jobs = job_list.find_all("li", class_="job-list-li")
        
        print(f"Found {len(jobs)} jobs on page 1.")

        for job in jobs:
            # --- Extract Title & Link ---
            h2_tag = job.find("h2")
            if not h2_tag:
                continue # Skip if no title
                
            a_tag = h2_tag.find("a")
            title = a_tag.text.strip()
            relative_link = a_tag['href']
            full_link = f"{base_url}{relative_link}"

            
            company = "Unknown"
            
            # Strategy A: Look for the logo container
            logo_div = job.find("li", class_="job-logo")
            if logo_div:
                img = logo_div.find("img")
                if img and 'alt' in img.attrs:
                    company = img['alt']
            
            Company.objects.get_or_create(name=company)


            # --- Extract Date / Location ---
            meta_div = job.find("li", class_="job-item")
            date_posted = meta_div.text.strip() if meta_div else "Recent"
            # get the full description
            full_description, application_url = scrape_job_details(full_link)
            if not full_description:
                job_description = job.find("li", class_="job-desc")
                full_description = job_description.text.strip() if job_description else ""
            
            final_external_url = application_url if application_url else full_link

            if not JobPosting.objects.filter(title=title, company__name=company).exists():
                job_posting = JobPosting(
                    title=title,
                    description=full_description,
                    company=Company.objects.get(name=company),
                    external_url=final_external_url,
                    is_external=True,
                    posted_at=date_posted
                )
                job_posting.save()

    except Exception as e:
        print(f"Error: {e}")