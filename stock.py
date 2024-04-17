from pyrogram import Client, filters
import pandas as pd
import finpy_tse as fpy


api_id = 27356729
api_hash = "2076532de16fc82d242fcc1a012ce5f1"
bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y"


# تعریف آرگومان های مورد نیاز
bot = Client("mtest bot" ,
            api_id = api_id ,
            api_hash = api_hash , 
            bot_token = bot_token ,
)


user_data = {}


# Read users.xlsx file
users_df = pd.read_excel('users.xlsx')

# Creating a list of allowed chat_ids
allowed_chat_ids = users_df['chat_id'].tolist()

# Define the command to view the desired share information
@bot.on_message(filters.command('stock') & filters.private)
def get_excel_info_command(client, message):
    if message.chat.id in allowed_chat_ids:
        message.reply_text("لطفا نام سهم مورد نظر را وارد کنید")
        user_data[message.chat.id] = {'state': 'waiting_for_stock_name'}
    else:
        message.reply_text("برای مشاهده اطلاعات سهام ها، ابتدا با دستور /register ثبت نام کنید")

# Receive share information and check the price and...
@bot.on_message(not filters.command and filters.create(lambda message, _: message.chat.id in user_data and user_data[message.chat.id]['state'] == 'waiting_for_stock_name'))
def handle_message1(client, message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id]['state'] == 'waiting_for_stock_name':
        customer_input = message.text
        
        user_data[chat_id]['state'] = 'processing'
    if chat_id in user_data and user_data[chat_id]['state'] == 'processing':
        try:
            
            MarketWatch = fpy.Get_MarketWatch()
            # Reading information from the dataframe
            df = MarketWatch[0].reset_index()

            
            if customer_input in df['Ticker'].values:
                    stock_Ticker = df.loc[df['Ticker'] == customer_input , 'Ticker'].values[0]
                    stock_Time = df.loc[df['Ticker'] == customer_input , 'Time'].values[0]
                    stock_Close = df.loc[df['Ticker'] == customer_input , 'Close'].values[0]
                    stock_Close_Percent = df.loc[df['Ticker'] == customer_input , 'Close(%)'].values[0]
                    stock_Market_Cap = df.loc[df['Ticker'] == customer_input , 'Market Cap'].values[0]
                    message.reply_text(f'''🕘زمان: {stock_Time}

📊نام سهم:  {stock_Ticker}

💵 قیمت: {stock_Close}

📉درصد تغییر: {stock_Close_Percent}

💰ارزش بازار : {stock_Market_Cap}''')
            else:
                    message.reply_text(f"سهم {customer_input} در لیست وجود ندارد.")

        except Exception as e:
            message.reply_text(f"خطایی رخ داد: {e}")
        user_data[chat_id]['state'] = 'complete'


bot.run()
