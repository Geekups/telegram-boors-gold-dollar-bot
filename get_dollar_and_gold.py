import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to get the current time
def get_current_time():
    # Get the current datetime
    now = datetime.now()
    # Extract hour, minute, and second
    hour = now.hour
    minute = now.minute
    second = now.second
    # Return the time as a tuple
    return hour, minute, second

# Function to get the dollar and gold prices in Iranian Toman for any given time
def get_prices():
    # Placeholder website URL
    url = "https://irarz.com/"
    
    # Make a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assuming the prices are in elements with specific IDs or classes
        # You'll need to inspect the website to find the correct selectors
        dollar_price_element = soup.find(id='usdmax')  # this is rial
        gold_price_element = soup.find(id='gold-price')
        
        if dollar_price_element and gold_price_element:
            # Extract the prices
            dollar_price = float(dollar_price_element.text)
            gold_price = float(gold_price_element.text)
            # Convert prices to Iranian Toman (assuming 1 USD = 10000 Toman and 1 gram of gold = 10000 Toman)
            dollar_price_toman = dollar_price * 10000
            gold_price_toman = gold_price * 10000
            return dollar_price_toman, gold_price_toman
        else:
            print("Failed to find price elements.")
            return None, None
    else:
        print("Failed to fetch page. Status code:", response.status_code)
        return None, None

# Example usage
# Get the current time
current_hour, current_minute, current_second = get_current_time()
print("Current time:", current_hour, ":", current_minute, ":", current_second)

# Get the dollar and gold prices for the current time
dollar_price, gold_price = get_prices()
if dollar_price and gold_price:
    print("Dollar price in Toman:", dollar_price)
    print("Gold price in Toman:", gold_price)
else:
    print("Failed to fetch prices.")
