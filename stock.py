from pyrogram import Client, filters
import anonsurf_handler
import stock_info

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

anonsurf_handler.start_anonsurf("90708060")

# Define the command to view the desired share information
@bot.on_message(filters.command('stock') & filters.private)
def get_excel_info_command(client, message):
        message.reply_text("لطفا نام سهم مورد نظر را وارد کنید")
        user_data[message.chat.id] = {'state': 'waiting_for_stock_name'}

# Receive share information and check the price and...
@bot.on_message(not filters.command and filters.create(lambda message, _: message.chat.id in user_data and user_data[message.chat.id]['state'] == 'waiting_for_stock_name'))
def handle_message1(client, message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id]['state'] == 'waiting_for_stock_name':
        customer_input = message.text
        
        user_data[chat_id]['state'] = 'processing'
    if chat_id in user_data and user_data[chat_id]['state'] == 'processing':
        try:
 
           message.reply_text(stock_info.get_stock_info(customer_input))
            


        except Exception as e:
            message.reply_text(f"خطایی رخ داد: {e}")
        user_data[chat_id]['state'] = 'complete'


bot.run()
