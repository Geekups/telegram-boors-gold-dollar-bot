from pyrogram import Client, filters
from pyrogram.types import Message , InlineKeyboardButton , InlineKeyboardMarkup
from tabulate import tabulate
import pandas as pd




api_id = 27356729
api_hash = "2076532de16fc82d242fcc1a012ce5f1"
bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y"


#Define required arguments
bot = Client("start bot" ,
            api_id = api_id ,
            api_hash = api_hash , 
            bot_token = bot_token ,
)

# Allowed list of admin usernames
admin_username = {
    'mostafa13438',
}

# Definition of the start command
@bot.on_message(filters.command('start') & filters.private)
def command1(bot , message):
    first_name= message.from_user.first_name
    bot.send_message(message.chat.id, f"سلام {first_name}! به ربات خوش اومدی.")

# Admin panel definition
@bot.on_message(filters.command('admin') & filters.private)
def admin_command(client, message):
    
    username = message.from_user.username
    
    if username in admin_username: # If the desired username was in the admin list, we give the user access to administrative commands
        
        keyboard = [
            [InlineKeyboardButton("دریافت اطلاعات مشتریان", callback_data='get_user_info')]
        ]
        reply_mark = InlineKeyboardMarkup(keyboard)
        message.reply_text("به پنل مدیریتی خوش آمدید", reply_markup=reply_mark)
    else: # If the desired username is not in the admin list, we will send an error message to the user
        
        message.reply_text("شما دسترسی به این دستور ندارید.")

# Send customer list to admin
@bot.on_callback_query(filters.regex('^get_user_info$'))
def get_user_info(client, callback_query):
    try:
        # Excel file path
        file_path = 'users.xlsx'

        # Reading customer information from an Excel file
        df = pd.read_excel(file_path ,usecols= ['name', 'phone', 'email'])


        # Set the output format using tabulate
        user_info_text = tabulate(df, headers=['name', 'phone', 'email'], tablefmt="grid")

        callback_query.message.edit_text(user_info_text)
        # Send the Excel file to the user
        client.send_document(chat_id=callback_query.message.chat.id, document=file_path)


    except Exception as e:
        callback_query.message.reply_text(f"خطایی رخ داد: {e}")

bot.run()
