import requests
from bs4 import BeautifulSoup

def get_stock_info(symbol):
    try:  
        # Base URL for the website
        base_url = "https://databourse.ir/symbol"
        # symbol = "فولاد"
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        # The URL for the stock information page
        # This is a placeholder. You'll need to find the correct URL structure for the stock pages.
        stock_url = f"{base_url}/{symbol}"
        
        # Make a request to the website
        response = requests.get(stock_url , headers= headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Use the CSS selector to find the element
            # Note: The CSS selector you provided is quite specific and might need adjustment
            # based on the actual structure of the website's HTML.
            stock_Ticker = soup.select_one("#content > div.symbol-information > div.symbol-info.symbol-box > div:nth-child(2) > div:nth-child(1) > span.txt")
            stock_Time = soup.select_one("#content > div.symbol-information > div:nth-child(4) > div.today-information.symbol-box > div:nth-child(2) > span.num")
            stock_end = soup.select_one("#content > div.symbol-information > div:nth-child(4) > div.today-information.symbol-box > div:nth-child(3) > span:nth-child(2)")
            stock_Close = soup.select_one("#content > div.symbol-information > div:nth-child(4) > div.today-information.symbol-box > div:nth-child(4) > span:nth-child(2)")
            stock_Close_Percent = soup.select_one("#content > div.symbol-information > div:nth-child(4) > div.today-information.symbol-box > div:nth-child(3) > span.num.green")
            stock_Market_Cap = soup.select_one("#content > div.symbol-information > div:nth-child(4) > div.today-information.symbol-box > div:nth-child(7) > span.num")
            if stock_end == "0":
                 return("خطا در دریافت اطلاعات.")

            # Extract and print the information
            else:
                return (f'''🕘آخرین زمان معاملاتی: {stock_Time}

    📊نام سهم:  {stock_Ticker}

    💵 قیمت: {stock_Close}

    📉درصد تغییر: %{stock_Close_Percent}

    💰ارزش بازار : {stock_Market_Cap}''')
    
    except :
                
            return (f"سهام {symbol} پیدا نشد")
    

