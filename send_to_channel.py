from pyrogram import Client
import asyncio
import time
import jdatetime
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


def channel_run():   
    # دریافت تاریخ امروز به صورت شمسی
    today_shamsi = jdatetime.date.today()

    # تبدیل تاریخ شمسی به میلادی
    today_gregorian = today_shamsi.togregorian()

    # تبدیل تاریخ میلادی به رشته برای استفاده در توابع
    start_date_str = today_shamsi.strftime('%Y-%m-%d')
    end_date_str = today_shamsi.strftime('%Y-%m-%d')



    chanel_chatid = -1002122878847

    bot = Client("my test bot" ,
                api_id = 27356729 ,
                api_hash = "2076532de16fc82d242fcc1a012ce5f1" , 
                bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y")


    def get_shakhes_info():
        try:  
            # Base URL for the website
            base_url = "https://databourse.ir"
            # symbol = "فولاد"
            
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
            # The URL for the stock information page
            # This is a placeholder. You'll need to find the correct URL structure for the stock pages.
            
            # Make a request to the website
            response = requests.get(base_url , headers= headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Use the CSS selector to find the element
                # Note: The CSS selector you provided is quite specific and might need adjustment
                # based on the actual structure of the website's HTML.
                shakhes = soup.select_one("#content > div.content-box > div:nth-child(1) > div:nth-child(2) > div.value").text
                arzesh = soup.select_one("#content > div.content-box > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)").text
                tedad= soup.select_one("#content > div.content-box > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(2)").text     
                hajm = soup.select_one("#content > div.content-box > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2)").text


                return shakhes , arzesh , tedad , hajm
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    shakhes ,  arzesh , tedad , hajm = get_shakhes_info()   

    async def send_message(shakhes , arzesh , tedad , hajm):
        await bot.send_message( chanel_chatid,       (f'''🔹شاخص کل: {shakhes}
    🔹تعداد معاملات:  {tedad}
    🔹حجم معاملات: {hajm}
    🔹ارزش بازار: {arzesh}'''))
    async def run_at_specific_times():
        
        try:
            while True:
                tehran_tz = pytz.timezone('Asia/Tehran')
                current_time = datetime.now(tehran_tz)

                if current_time.hour == 10 or (current_time.hour == 11 and current_time.minute == 30) or (current_time.hour == 12 and current_time.minute == 30):
                    shakhes ,  arzesh , tedad , hajm = get_shakhes_info()   
                    await send_message(shakhes , arzesh , tedad , hajm)
                    # انتظار 1 دقیقه قبل از بررسی مجدد زمان
                    await asyncio.sleep(60)
                else:
                    await asyncio.sleep(60)


        except Exception as e:
            print(f"An error occurred: {e}")

    # اجرای تابع با استفاده از asyncio
    async def main():
        await run_at_specific_times()


    bot.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    bot.stop()








