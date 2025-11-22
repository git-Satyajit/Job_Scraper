import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

def scrape_naukri(base_url):
    """
    Scrapes job listings from Naukri.com with 0-2 years of experience.

    Args:
        base_url (str): The initial URL to start scraping from.

    Returns:
        list: A list of dictionaries, where each dictionary represents a job.
    """
    print("🚀 Starting Naukri scraper...")
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Execute script to hide webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    jobs_list = []
    seen_jobs = set()  # Track unique jobs to avoid duplicates
    
    # If no URL is provided, use a default URL for 0-2 years experience jobs
    if not base_url.strip():
        base_url = "https://www.naukri.com/jobs-0-to-2-years-experience"
    
    # Logic to handle URL structure
    url_prefix = base_url.strip()
    
    # If the URL doesn't already include experience filter, add it
    if "0-to-2-years" not in url_prefix.lower() and "experience" not in url_prefix.lower():
        if "?" in url_prefix:
            url_prefix += "&experience=0-2%20years"
        else:
            url_prefix += "?experience=0-2%20years"

    # Start with the initial URL
    current_url = url_prefix
    visited_urls = set()
    
    page_count = 1
    
    while current_url and len(jobs_list) < 50 and page_count <= 15:  # Limit to 15 pages
        if current_url in visited_urls:
            break
            
        visited_urls.add(current_url)
        print(f"Scraping page {page_count}: {current_url}")
        
        try:
            driver.get(current_url)
            
            # Wait for page to load and handle dynamic content
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "article, div[data-job-id], .jobTuple, .job-tuple"))
                )
            except:
                print("Waiting for page elements to load...")
                time.sleep(8)  # Fallback wait
            
            # Scroll to load more content if needed
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            # Try different selectors as Naukri's HTML structure might have changed
            job_elements = soup.select('article.jobTuple, div.jobTuple, div.job-tuple, div[data-job-id], .srp-jobtuple-wrapper, .jobTupleHeader')

            if not job_elements:
                print("No more job listings found. Stopping.")
                break
                
            print(f"Found {len(job_elements)} job elements on page {page_count}")

            for job in job_elements:
                # Try different selectors for title
                title_element = (
                    job.select_one('a.title') or 
                    job.select_one('a.jobTitle') or 
                    job.select_one('a[title]') or
                    job.select_one('a.job-title')
                )
                title = title_element.get_text(strip=True) if title_element else "N/A"
                
                # Try different selectors for company with more comprehensive approach
                company_element = (
                    job.select_one('a.subTitle') or 
                    job.select_one('a.companyName') or 
                    job.select_one('a.company-name') or
                    job.select_one('div.company-name') or
                    job.select_one('div.companyInfo span.subTitle') or
                    job.select_one('span.companyName') or
                    job.select_one('[title*="company"]') or
                    job.select_one('.comp-name') or
                    job.select_one('.company') or
                    job.select_one('span.subTitle') or
                    job.select_one('div.subTitle')
                )
                company = company_element.get_text(strip=True) if company_element else "N/A"
                
                # Enhanced company name extraction
                if company == "N/A" or len(company) < 2:
                    # Look for company info in different patterns
                    company_patterns = [
                        r'([A-Z][a-zA-Z\s&.,-]+(?:Ltd|Limited|Inc|Corp|Company|Technologies|Solutions|Systems|Services|Pvt|Private))',
                        r'([A-Z][a-zA-Z\s&.,-]{2,30}(?:\s+(?:Ltd|Limited|Inc|Corp|Company|Technologies|Solutions|Systems|Services|Pvt|Private))?)',
                    ]
                    
                    job_text = job.get_text()
                    for pattern in company_patterns:
                        matches = re.findall(pattern, job_text)
                        if matches:
                            # Filter out common non-company words
                            excluded_words = ['Experience', 'Years', 'Salary', 'Location', 'Posted', 'Apply', 'Job', 'Role', 'Position']
                            for match in matches:
                                if not any(word in match for word in excluded_words) and len(match.strip()) > 2:
                                    company = match.strip()
                                    break
                            if company != "N/A":
                                break
                
                # Final fallback - look for elements with company-related classes or text
                if company == "N/A" or len(company) < 2:
                    for element in job.select('span, div, a, p'):
                        element_text = element.get_text(strip=True)
                        element_classes = element.get('class', [])
                        
                        # Check if element has company-related class or contains company info
                        if (any('company' in str(cls).lower() for cls in element_classes) or
                            any('subtitle' in str(cls).lower() for cls in element_classes)):
                            if len(element_text) > 2 and len(element_text) < 100:
                                company = element_text
                                break
                
                # Try different selectors for location
                location_element = (
                    job.select_one('span.locWdth') or 
                    job.select_one('span.location') or 
                    job.select_one('li.location') or
                    job.select_one('div.location')
                )
                location = location_element.get_text(strip=True) if location_element else "N/A"
                
                # Try different selectors for link
                if title_element and title_element.has_attr('href'):
                    link = title_element['href']
                else:
                    link_element = job.select_one('a[href]')
                    link = link_element['href'] if link_element else "#"
                
                # Extract experience information - try different selectors
                experience_element = (
                    job.select_one('li.experience') or 
                    job.select_one('span.experience') or 
                    job.select_one('div.experience') or
                    job.select_one('[title*="experience"]')
                )
                experience = experience_element.get_text(strip=True) if experience_element else "N/A"
                
                # If no experience info found in dedicated element, try to find it in the job description
                if experience == "N/A":
                    job_text = job.get_text(strip=True).lower()
                    exp_match = re.search(r'(\d+)\s*-?\s*(\d*)\s*years?\s*(?:of)?\s*experience', job_text)
                    if exp_match:
                        min_exp = int(exp_match.group(1))
                        max_exp = int(exp_match.group(2)) if exp_match.group(2) else min_exp
                        experience = f"{min_exp}-{max_exp} years" if exp_match.group(2) else f"{min_exp} years"
                
                # Check if the job is for 0-2 years of experience
                # Using regex to match patterns like "0-1 yrs", "1-2 years", "2 years", etc.
                if experience != "N/A":
                    exp_match = re.search(r'(\d+)\s*-?\s*(\d*)\s*y', experience.lower())
                    if exp_match:
                        min_exp = int(exp_match.group(1))
                        max_exp = int(exp_match.group(2)) if exp_match.group(2) else min_exp
                        
                        # Skip jobs requiring more than 2 years of experience
                        if min_exp > 2:
                            continue
                
                # Create a unique identifier for the job to avoid duplicates
                job_id = f"{title.lower().strip()}_{company.lower().strip()}_{location.lower().strip()}"
                
                if job_id not in seen_jobs:
                    seen_jobs.add(job_id)
                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "link": link,
                        "experience": experience,
                        "source": "Naukri"
                    }
                    jobs_list.append(job_data)
                    print(f"Added job: {title} at {company}")
                else:
                    print(f"Duplicate job skipped: {title} at {company}")
                
                if len(jobs_list) >= 50:
                    break
            
            # Find the next page URL dynamically
            next_url = None
            try:
                # Try multiple selectors for the next button
                next_selectors = [
                    "//a[contains(@class, 'fright') and contains(text(), 'Next')]",
                    "//a[contains(text(), 'Next')]",
                    "//a[contains(@class, 'next')]",
                    "//span[contains(@class, 'np') and contains(@class, 'fright')]/a",
                    "//div[contains(@class, 'pagination')]//a[last()]"
                ]
                
                for selector in next_selectors:
                    try:
                        next_button = driver.find_element(By.XPATH, selector)
                        next_url = next_button.get_attribute('href')
                        if next_url and next_url != current_url:
                            print(f"Found next page URL: {next_url}")
                            break
                    except:
                        continue
                        
                if not next_url:
                    # Try to construct next page URL based on current URL pattern
                    if "pageno=" in current_url:
                        current_page = re.search(r'pageno=(\d+)', current_url)
                        if current_page:
                            next_page_num = int(current_page.group(1)) + 1
                            next_url = re.sub(r'pageno=\d+', f'pageno={next_page_num}', current_url)
                    elif "/jobs-" in current_url and current_url.endswith(f'-{page_count}'):
                        next_url = current_url.replace(f'-{page_count}', f'-{page_count + 1}')
                    elif not any(char.isdigit() for char in current_url.split('/')[-1]):
                        next_url = f"{current_url}-{page_count + 1}"
                        
            except Exception as e:
                print(f"Error finding next page: {e}")
            
            current_url = next_url
            page_count += 1

        except Exception as e:
            print(f"An error occurred on page {page_count}: {e}")
            break
            
    driver.quit()
    print(f"✅ Found {len(jobs_list)} jobs on Naukri.")
    return jobs_list