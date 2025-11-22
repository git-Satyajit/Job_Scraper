import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

def scrape_indeed(base_url):
    """
    Scrapes job listings from Indeed.com with 0-2 years of experience.

    Args:
        base_url (str): The initial URL to start scraping from.

    Returns:
        list: A list of dictionaries, where each dictionary represents a job.
    """
    print("🚀 Starting Indeed scraper...")
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    jobs_list = []
    
    # If no URL is provided, use a default URL for entry-level jobs
    if not base_url.strip():
        base_url = "https://in.indeed.com/jobs?q=&l=&sc=0kf%3Aattr%28FSME%29%3B"
    
    # Ensure the URL includes experience filter for 0-2 years
    if "attr(FSME)" not in base_url and "explvl=entry_level" not in base_url:
        if "?" in base_url:
            base_url += "&explvl=entry_level"
        else:
            base_url += "?explvl=entry_level"
    
    for page_num in range(0, 15): # Scrape up to 15 pages
        if len(jobs_list) >= 50:
            break

        # Indeed uses 'start' parameter for pagination (0, 10, 20...)
        start_index = page_num * 10
        current_url = f"{base_url}&start={start_index}"
        print(f"Scraping page {page_num + 1}: {current_url}")

        try:
            driver.get(current_url)
            # Wait for job results to load
            time.sleep(5)  # Increase wait time to ensure page loads
            
            # Try different selectors as Indeed's HTML structure might have changed
            soup = BeautifulSoup(driver.page_source, 'lxml')
            job_cards = soup.select('div.job_seen_beacon, div.cardOutline, div.job_seen_beacon, div[data-testid="jobListing"]')

            if not job_cards:
                print("No more job listings found. Stopping.")
                break

            for card in job_cards:
                # Try different selectors for title as the HTML structure might vary
                title_element = (
                    card.select_one('h2.jobTitle > a') or 
                    card.select_one('h2 > a') or 
                    card.select_one('h2 a') or
                    card.select_one('a[data-jk]')
                )
                
                if title_element:
                    title = title_element.get_text(strip=True).replace("new", "")
                else:
                    # Try to find any heading that might contain the job title
                    title_element = card.select_one('h2') or card.select_one('h3')
                    title = title_element.get_text(strip=True).replace("new", "") if title_element else "N/A"
                
                # Try different selectors for company name
                company_element = (
                    card.select_one('span.companyName') or 
                    card.select_one('span.company') or 
                    card.select_one('div.company') or
                    card.select_one('[data-testid="company-name"]')
                )
                company = company_element.get_text(strip=True) if company_element else "N/A"
                
                # Try different selectors for location
                location_element = (
                    card.select_one('div.companyLocation') or 
                    card.select_one('div.location') or 
                    card.select_one('span.location') or
                    card.select_one('[data-testid="text-location"]')
                )
                location = location_element.get_text(strip=True) if location_element else "N/A"
                
                # Try to extract experience information from various description elements
                job_description = ""
                description_element = (
                    card.select_one('div.job-snippet') or 
                    card.select_one('div.summary') or 
                    card.select_one('.job-snippet') or
                    card.select_one('[data-testid="job-description"]')
                )
                if description_element:
                    job_description = description_element.get_text(strip=True)
                
                # Look for experience requirements in the job description
                experience = "Entry Level"
                exp_pattern = re.search(r'(\d+)\s*-?\s*(\d*)\s*years?\s*(?:of)?\s*experience', job_description.lower())
                if exp_pattern:
                    min_exp = int(exp_pattern.group(1))
                    max_exp = int(exp_pattern.group(2)) if exp_pattern.group(2) else min_exp
                    
                    # Skip jobs requiring more than 2 years of experience
                    if min_exp > 2:
                        continue
                    experience = f"{min_exp}-{max_exp} years" if exp_pattern.group(2) else f"{min_exp} years"
                
                # Get the link - try different approaches
                if title_element and title_element.has_attr('href'):
                    link = title_element['href']
                    if not link.startswith('http'):
                        link = "https://in.indeed.com" + link
                else:
                    # Try to find any link in the card
                    link_element = card.select_one('a[href]')
                    link = link_element['href'] if link_element else "#"
                    if link != "#" and not link.startswith('http'):
                        link = "https://in.indeed.com" + link

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                    "experience": experience,
                    "source": "Indeed"
                }
                jobs_list.append(job_data)

                if len(jobs_list) >= 50:
                    break
                    
        except Exception as e:
            print(f"An error occurred on page {page_num + 1}: {e}")
            break
    
    driver.quit()
    print(f"✅ Found {len(jobs_list)} jobs on Indeed.")
    return jobs_list