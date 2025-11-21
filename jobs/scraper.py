import requests
from bs4 import BeautifulSoup
from .models import JobPosting
from users.models import Company

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
            job_description = job.find("li", class_="job-desc")
            description_text = job_description.text.strip() if job_description else ""

            if not JobPosting.objects.filter(title=title, company__name=company).exists():
                job_posting = JobPosting(
                    title=title,
                    description=description_text,
                    company=Company.objects.get(name=company),
                    external_url=full_link,
                    is_external=True,
                    posted_at=date_posted
                )
                job_posting.save()

    except Exception as e:
        print(f"Error: {e}")