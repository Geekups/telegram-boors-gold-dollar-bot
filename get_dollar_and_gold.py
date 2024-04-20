import requests
from bs4 import BeautifulSoup
from arabic_reshaper import reshape
from bidi.algorithm import get_display


def convert_farsi_to_english(farsi_text):
    # Reshape the Farsi text
    reshaped_text = reshape(farsi_text)
    
    # Reorder the reshaped text
    bidi_text = get_display(reshaped_text)
    
    return bidi_text

# Function to get the dollar and gold prices in Iranian Toman for any given time
def get_prices():
    # Placeholder website URL
    url = "https://irarz.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
    # Make a request to the website
    response = requests.get(url , headers= headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assuming the prices are in elements with specific IDs or classes
        # You'll need to inspect the website to find the correct selectors
        dollar_price_element = soup.find(id='usdmax')
        gold_price_element = soup.find(id='geram24')
        
        if dollar_price_element and gold_price_element:
            # Extract the prices
            dollar_price = convert_farsi_to_english(dollar_price_element.text)
            gold_price = convert_farsi_to_english(gold_price_element.text)
           
            return dollar_price, gold_price # all prices are in "Rial"
        else:
            print("Failed to find price elements.")
            return None, None
    else:
        print("Failed to fetch page. Status code:", response.status_code)
        return None, None

# Get the dollar and gold prices for the current time
dollar_price, gold_price = get_prices()
if dollar_price and gold_price:
    print(dollar_price)
    print(gold_price)
else:
    print("Failed to fetch prices.")
