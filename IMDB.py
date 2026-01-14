import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_imdb_top_250():
    # 1. Setup Chrome Options for Headless Mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs without opening a browser window [cite: 15, 16]
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Adding a user-agent to mimic a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 2. Initialize WebDriver with auto-downloading ChromeDriver [cite: 28, 31]
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    movie_data = []

    try:
        # 3. Load IMDb Top 250 Page [cite: 9]
        print("Connecting to IMDb...")
        driver.get("https://www.imdb.com/chart/top/")
        
        # Give the page time to load dynamic JavaScript content [cite: 26, 36]
        time.sleep(5)

        # 4. Extract Movie Elements
        # IMDb uses a specific structure for its Top 250 list items
        movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

        print(f"Found {len(movies)} movies. Starting extraction...")

        for index, movie in enumerate(movies):
            try:
                # Extract Title and Ranking [cite: 4, 11]
                title_text = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
                # Format is usually "1. The Shawshank Redemption"
                ranking = title_text.split('.')[0]
                name = title_text.split('.', 1)[-1].strip()

                # Extract Year [cite: 11]
                metadata = movie.find_elements(By.CSS_SELECTOR, "span.cli-title-metadata-item")
                year = metadata[0].text if len(metadata) > 0 else "N/A"

                # Extract Rating [cite: 4, 11]
                rating_element = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
                rating = rating_element.text

                movie_data.append({
                    "Ranking": ranking,
                    "Title": name,
                    "Year": year,
                    "IMDb Rating": rating
                })
            except Exception as e:
                continue # Skip if an individual movie fails to load

    finally:
        # 5. Close the browser
        driver.quit()

    # 6. Save data to CSV [cite: 14, 25, 33]
    if movie_data:
        df = pd.DataFrame(movie_data)
        filename = "imdb_top_250_ratings.csv"
        df.to_csv(filename, index=False)
        print(f"Successfully saved {len(df)} movies to '{filename}'.")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    scrape_imdb_top_250()