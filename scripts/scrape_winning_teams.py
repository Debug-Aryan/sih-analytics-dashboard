from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

url = "https://sih.gov.in/sih2025/sih2025-grand-finale-result"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    page.goto(url, wait_until="networkidle")
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, "html.parser")

# ✅ Target table by ID
table = soup.find("table", id="sheet0")
tbody = table.find("tbody")

rows = []

def get_col(tr, col_class):
    td = tr.find("td", class_=col_class)
    return td.get_text(strip=True) if td else None

# ✅ Iterate ALL rows (row0 + row1)
for tr in tbody.find_all("tr"):
    tds = tr.find_all("td")
    if not tds:
        continue  # skip empty/header rows

    rows.append({
        "ps_id": get_col(tr, "column1"),
        "team_id": get_col(tr, "column5"),
        "idea_id": get_col(tr, "column6"),
        "team_name": get_col(tr, "column7"),
        "status": get_col(tr, "column9"),
        "prize_money": get_col(tr, "column10"),
    })

df = pd.DataFrame(rows)

# Drop rows where ps_id is missing (safety)
df = df[df["ps_id"].notna()]

df.to_csv("sih_2025_grand_finale_result_clean.csv", index=False)

print("✅ CSV saved successfully")
print("✅ Rows scraped:", len(df))
print(df.head())
