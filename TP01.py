import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com"

all_books = []

page_number = 1

while True:

    url = f"{BASE_URL}/catalogue/page-{page_number}.html"

    print(f"Scraping page {page_number}: {url}")

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    if response.status_code != 200:
        print("Error:", response.status_code)
        break

    # ==========================================
    # Question 1: Display HTML source code
    # ==========================================

    print("\n===== HTML SOURCE CODE =====")
    print(response.text[:2000])
    print("============================\n")

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # ==========================================
    # Question 2: Extract books
    # ==========================================

    books = soup.find_all("article", class_="product_pod")

    if not books:
        print("No more books found.")
        break

    for book in books:

        # Book title
        title = book.find("h3").find("a")["title"]

        # Price
        price = book.find("p", class_="price_color").get_text(strip=True)

        # Availability
        availability = book.find(
            "p",
            class_="instock availability"
        ).get_text(strip=True)

        # Rating
        rating = book.find("p", class_="star-rating")

        if rating:
            rating = rating.get("class")[1]
        else:
            rating = "Unknown"

        # Book URL
        book_url = book.find("h3").find("a")["href"]

        all_books.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "URL": book_url,
            "Page": page_number
        })

    page_number += 1

    time.sleep(0.5)


# ==========================================
# Question 3: Save results to CSV
# ==========================================

df = pd.DataFrame(all_books)

df.to_csv(
    "books.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# Question 4: Check number of rows
# ==========================================

print("\n================================")
print("Scraping completed!")
print("Total books:", len(df))
print("CSV file: books.csv")
print("================================")

if len(df) >= 1000:
    print("SUCCESS: The CSV contains at least 1000 rows.")
else:
    print("WARNING: Less than 1000 rows.")