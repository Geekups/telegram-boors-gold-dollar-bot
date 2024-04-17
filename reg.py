from pyrogram import Client, filters
import pandas as pd
import os

api_id = 27356729
api_hash = "2076532de16fc82d242fcc1a012ce5f1"
bot_token = "6872044004:AAETNHH9kO-XnzfyeIIq1oTRNQNN4lnNr2Y"


# Define required arguments
bot = Client("register" ,
            api_id = api_id ,
            api_hash = api_hash , 
            bot_token = bot_token ,
)


user_data = {}

# Definition of registration command
@bot.on_message(filters.command('register') & filters.private)
def register_command(client , message):

    message.reply_text("لطفا نام و نام خانوادگی خود را وارد نمائید:")
    user_data[message.chat.id] = {'state': 'waiting_for_name'}

@bot.on_message(not filters.command and filters.private)

def handle_message(client , message):
    chat_id = message.chat.id
    if chat_id in user_data:
        state = user_data[chat_id]['state']
        if state == 'waiting_for_name':
            user_data[chat_id]['name'] = message.text
            user_data[chat_id]['state'] = 'waiting_for_phone'
            message.reply_text("شماره تلفن خود را وارد نمائید:")
        elif state == 'waiting_for_phone':
            user_data[chat_id]['phone'] = message.text
            user_data[chat_id]['state'] = 'waiting_for_age'
            message.reply_text("سن خود را وارد نمائید:")
        elif state == 'waiting_for_age':
            user_data[chat_id]['age'] = message.text
            user_data[chat_id]['state'] = 'waiting_for_email'
            message.reply_text("آدرس ایمیل خود را وارد کنید:")
        elif state == 'waiting_for_email':
            user_data[chat_id]['email'] = message.text
            user_data[chat_id]['state'] = 'complete'
            user_data[chat_id]['chat_id'] = message.chat.id
            save_user_data(chat_id)
            message.reply_text("✅اطلاعات شما با موفقیت ثبت شد!")
            del user_data[chat_id]
        
        # Delete the registered information if there is a problem
        else:
            message.reply_text("❌مشکل در پردازش اطلاعات! لطفا مراحل ثبت نام را مجدداً طی کنید")
            del user_data[chat_id]

# Save user information in Excel file
def save_user_data(chat_id):
    user_info = user_data[chat_id]
    # If the Excel file does not exist, we will create it
    if not os.path.exists('users.xlsx'):
        df = pd.DataFrame(columns=['name', 'phone', 'age', 'email', 'chat_id'])
    else:
        df = pd.read_excel('users.xlsx')
    # Convert Dictionary to DataFrame
    user_info_df = pd.DataFrame([user_info])
    # We add customer information to the main dataframe
    df = pd.concat([df, user_info_df], ignore_index=True)
    # We save the dataframe in the Excel file
    df.to_excel('users.xlsx', index=False)

bot.run()
