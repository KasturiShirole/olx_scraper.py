
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Setup
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
driver = webdriver.Chrome(options=options)

# Load OLX car cover search results
url = "https://www.olx.in/items/q-car-cover"
driver.get(url)
time.sleep(5)  # Allow time for page to load

# Scroll to load more items (optional, OLX may lazy load content)
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Extract listings
titles = []
prices = []

items = driver.find_elements(By.XPATH, '//li[contains(@class, "EIR5N")]')
for item in items:
    try:
        title = item.find_element(By.TAG_NAME, "span").text
        price = item.find_element(By.XPATH, './/span[contains(text(), "₹")]').text
        titles.append(title)
        prices.append(price)
    except:
        continue

driver.quit()

# Save to file
df = pd.DataFrame({'Title': titles, 'Price': prices})
df.to_csv('olx_car_covers.csv', index=False)
print("Scraped data saved to olx_car_covers.csv")
