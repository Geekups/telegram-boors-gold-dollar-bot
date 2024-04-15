from pyrogram import Client, filters
from pyrogram.types import Message , InlineKeyboardButton , InlineKeyboardMarkup
from tabulate import tabulate
import pandas as pd
import os
import time
import finpy_tse as fpy



api_id = 27356729
api_hash = "2076532de16fc82d242fcc1a012ce5f1"
bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y"


# تعریف آرگومان های مورد نیاز
bot = Client("mtest bot" ,
            api_id = api_id ,
            api_hash = api_hash , 
            bot_token = bot_token ,
            # proxy= proxy1

)


user_data = {}
admin_info = {}

# لیست مجاز chat_id های ادمین
admin_chat_ids = {
    181122579, # مثال: شماره تلفن ادمین را به عنوان chat_id در نظر بگیرید
    # اضافه کردن بیشتر chat_id های ادمین در اینجا
}

# تعریف دستور start
@bot.on_message(filters.command('start') & filters.private)
def command1(bot , message):
    first_name= message.from_user.first_name
    bot.send_message(message.chat.id, f"سلام {first_name}! به ربات خوش اومدی.")

# تعریف پنل کاربری
@bot.on_message(filters.command('admin') & filters.private)
def admin_command(client, message):
    
    chat_id = message.chat.id
    
    if chat_id in admin_chat_ids: # اگر chat_id مورد نظر در لیست ادمین بود، دسترسی به دستورات مدیریتی را به کاربر می‌دهیم
        
        keyboard = [
            [InlineKeyboardButton("دریافت اطلاعات مشتریان", callback_data='get_user_info')]
        ]
        reply_mark = InlineKeyboardMarkup(keyboard)
        message.reply_text("به پنل مدیریتی خوش آمدید", reply_markup=reply_mark)
    else: # اگر chat_id مورد نظر در لیست ادمین نبود، پیام خطا را به کاربر می‌فرستیم
        
        message.reply_text("شما دسترسی به این دستور ندارید.")

# ارسال لیست مشتریان برای ادمین
@bot.on_callback_query(filters.regex('^get_user_info$'))
def get_user_info(client, callback_query):
    try:
        # خواندن اطلاعات مشتریان از فایل اکسل
        df = pd.read_excel('users.xlsx')
        # تنظیم فرمت خروجی با استفاده از tabulate
        user_info_text = tabulate(df, headers='keys', tablefmt='grid', numalign="right", stralign="center")
        callback_query.message.reply_text(user_info_text)

        # ارسال فایل اکسل به کاربر
        file_path = 'users.xlsx'
        client.send_document(chat_id=callback_query.message.chat.id, document=file_path)

    except Exception as e:
        callback_query.message.reply_text(f"خطایی رخ داد: {e}")

bot.run()
