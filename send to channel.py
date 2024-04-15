from pyrogram import Client
import finpy_tse as fpy
import asyncio
import time
import jdatetime

start_time = time.time()

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
            bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y" ,

)


async def get_shakhes():
    try:
        shakhes = fpy.Get_CWI_History(
            start_date=start_date_str,
            end_date=end_date_str,
            ignore_date=False,
            just_adj_close=False,
            show_weekday=False,
            double_date=False)
        if shakhes.empty:
            return "تعطیل"
        f_hamvazn =  float(shakhes['Adj Close'].iloc[0])
        return f_hamvazn
    except Exception as e:
        if "Unknown datetime string format" in str(e):
            return "تعطیل"
        else:
            raise e
    

async def get_hamvazn():
    try:
        hamvazn = fpy.Get_EWI_History(
            start_date=start_date_str,
            end_date=end_date_str,
            ignore_date=False,
            just_adj_close=False,
            show_weekday=False,
            double_date=False)
        if hamvazn.empty:
            return "تعطیل"
        return float(hamvazn['Adj Close'].iloc[0])
    except Exception as e:
        if "Unknown datetime string format" in str(e):
            return "تعطیل"
        else:
            return e

        

async def get_vazni():
    try:
        vazni_arzeshi = fpy.Get_CWPI_History(
            start_date=start_date_str,
            end_date=end_date_str,
            ignore_date=False,
            just_adj_close=False,
            show_weekday=False,
            double_date=False)
        if vazni_arzeshi.empty:
            return "تعطیل"
        return float(vazni_arzeshi['Adj Close'].iloc[0])
    except Exception as e:
        if "Unknown datetime string format" in str(e):
            return "تعطیل"
        else:
            return e
        



async def boors_information():
    f_shakhes , f_hamvazn , f_vazni_arzeshi = await asyncio.gather(
        get_shakhes(), 
        get_hamvazn(),
        get_vazni()
    )
    return f_shakhes, f_hamvazn , f_vazni_arzeshi


async def send_message(f_hamvazn , f_shakhes , f_vazni_arzeshi):
    await bot.send_message(chanel_chatid , f'''🔹شاخص کل: {f_shakhes}
🔹شاخص هم وزن:  {f_hamvazn}
🔹وزنی-ارزشی: {f_vazni_arzeshi}''')
   
async def send_message_at_specific_times():
    while True:
        current_time = jdatetime.datetime.now().time()
        if current_time.hour == 10 or (current_time.hour == 9 and current_time.minute == 45) or (current_time.hour == 12 and current_time.minute == 34):
            f_shakhes , f_hamvazn , f_vazni_arzeshi = await boors_information()
            if f_shakhes != "تعطیل" and f_hamvazn != "تعطیل" and f_vazni_arzeshi != "تعطیل":
                await send_message(f_hamvazn , f_shakhes , f_vazni_arzeshi)
        else:
            # اگر س��عت فعلی برابر با 10 صبح نباشد، منتظر بمانید تا ساعت 10 صبح روز بعد فرا رسد
            await asyncio.sleep(60) # منتظر می‌مانیم تا یک دقیقه بعد بررسی کنیم

async def main():
    await send_message_at_specific_times()


bot.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
bot.stop()

end_time = time.time()

ex_time = end_time - start_time

print(ex_time)


