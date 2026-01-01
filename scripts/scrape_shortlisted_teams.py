from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

batches_to_scrape = [1, 2, 3, 4]

with sync_playwright() as p:
    print("Launching browser...")

    browser = p.chromium.launch(headless=False)  # set False to watch; True to hide
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")

    for batch_num in batches_to_scrape:
        url = f"https://sih.gov.in/sih2025/screeningresult-batch{batch_num}"
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle")
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        print(f"Tables found in batch {batch_num}:", len(tables))
        target = tables[0]

        rows = []
        for tr in target.find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cols: 
                rows.append(cols)

        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.columns = ["ps_id","organization","department","serial_no","idea_id","team_id","team_name","team_leader_name","aishe_code","institute_name","institute_city","institute_state","status"]
        csv_filename = f"sih_2025_shortlisted_batch{batch_num}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Saved CSV for batch {batch_num} with {len(df)} rows")

    browser.close()
    print("All batches processed and browser closed.")


