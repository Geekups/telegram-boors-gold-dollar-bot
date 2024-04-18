from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to get the dollar and gold prices in Iranian Toman for any given time
def get_prices():
    # Placeholder website URL
    url = "https://irarz.com/"
    
    # Initialize the WebDriver (replace 'webdriver.Chrome()' with 'webdriver.Firefox()' for Firefox)
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the website
        driver.get(url)
        
        # Assuming the prices are in elements with specific IDs or classes
        # You'll need to inspect the website to find the correct selectors
        dollar_price_element = driver.find_element(By.ID, 'usdmax') # this is rial
        gold_24_price_element = driver.find_element(By.ID, 'geram24')
        
        if dollar_price_element and gold_24_price_element:
            # Extract the prices
            dollar_price = float(dollar_price_element.text) # this is rial
            gold_price = float(gold_24_price_element.text) # this is rial
            # Convert prices to Iranian Toman (assuming 1 USD = 10000 Toman and 1 gram of gold = 10000 Toman)
            dollar_price_toman = dollar_price / 10000 # Assuming 1 Rial = 10000 Toman
            gold_price_toman = gold_price / 10000 # Assuming 1 Rial = 10000 Toman
            return dollar_price_toman, gold_price_toman
        else:
            print("Failed to find price elements.")
            return None, None
    finally:
        # Close the browser window
        driver.quit()

# Get the dollar and gold prices for the current time
dollar_price, gold_price = get_prices()
if dollar_price and gold_price:
    print("Dollar price in Toman:", dollar_price)
    print("Gold price in Toman:", gold_price)
else:
    print("Failed to fetch prices.")
