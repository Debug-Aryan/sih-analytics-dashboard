from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://sih.gov.in/sih2025PS" 

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print(f"Navigating to {url}...")
    page.goto(url)

    print("Waiting for initial table data...")
    try:
        page.wait_for_selector("#dataTablePS tbody tr td", timeout=20000)
        time.sleep(3) 
    except:
        print("Timeout waiting for data.")
        browser.close()
        exit()

    all_scraped_rows = []
    page_num = 1

    while True:
        print(f"--- Processing Page {page_num} ---")
        
        # 1. Grab current HTML
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        target_table = soup.find("table", {"id": "dataTablePS"})
        
        # 2. Extract Rows from this page
        if target_table and target_table.find("tbody"):
            current_page_rows = target_table.find("tbody").find_all("tr")
            print(f"Found {len(current_page_rows)} rows on this page.")
            
            for tr in current_page_rows:
                tds = tr.find_all("td")
                
                # Using the indices verified in your previous debug output
                if len(tds) >= 17:
                    # --- TITLE (Index 2) ---
                    title_td = tds[2]
                    hidden_div = title_td.find("div", class_="modal")
                    if hidden_div:
                        hidden_div.decompose()
                    title_text = title_td.get_text(strip=True)

                    # --- OTHER COLUMNS (Indices 13, 14, 15, 16) ---
                    category = tds[13].get_text(strip=True)
                    ps_number = tds[14].get_text(strip=True)
                    submissions = tds[15].get_text(strip=True)
                    theme = tds[16].get_text(strip=True)

                    all_scraped_rows.append([title_text, category, ps_number, submissions, theme])
        
        # 3. Handle Pagination (Clicking "Next")
        # We look for the "Next" button. In DataTables, it usually has ID 'dataTablePS_next'
        # or class 'paginate_button page-item next'.
        
        # Check if "Next" button exists and is NOT disabled
        next_button = page.locator("#dataTablePS_next:not(.disabled) a")
        
        if next_button.count() > 0:
            print("Clicking 'Next'...")
            next_button.click()
            
            # CRITICAL: Wait for new data to load
            time.sleep(3) 
            page_num += 1
        else:
            print("No more pages (or 'Next' button is disabled). Finishing up.")
            break

    browser.close()

# --- SAVE ALL DATA ---
if all_scraped_rows:
    columns = [
        "problem_statement_title",
        "category",
        "ps_number",
        "total_submission",
        "theme"
    ]
    
    df = pd.DataFrame(all_scraped_rows, columns=columns)
    
    # Remove duplicates just in case
    df.drop_duplicates(subset=['ps_number'], inplace=True)
    
    filename = "sih_2025_all_pages.csv"
    df.to_csv(filename, index=False)
    print(f"\nSUCCESS! Scraped {len(df)} unique rows across {page_num} pages.")
    print(f"Saved to '{filename}'")
else:
    print("No rows extracted.")