from pyrogram import Client, filters
from pyrogram.types import Message , InlineKeyboardButton , InlineKeyboardMarkup
from tabulate import tabulate
import pandas as pd
from stock import stock_run

import getpass
from telethon import TelegramClient, sync
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact, InputUser

def start_run():
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
            'username',
        }

        # Definition of the start command
        @bot.on_message(filters.command('start') & filters.private)
        def command1(bot , message):
            first_name= message.from_user.first_name
            keyboard = [
                    [InlineKeyboardButton("دریافت اطلاعات مشتریان", callback_data='reg_button'),
                    InlineKeyboardButton("ارسال پیام دسته جمعی" , callback_data='send_msg')]
                ]     
            reply_marks = InlineKeyboardMarkup(keyboard)       
            message.reply_text(f"سلام {first_name}! به ربات خوش اومدی.", reply_markup=reply_marks)
        
        @bot.on_callback_query(filters.regex('reg_button$'))
        def say_reg(client, callback_query):
            callback_query.message.reply_text("/register")



        # Admin panel definition
        @bot.on_message(filters.command('admin') & filters.private)
        def admin_command(client, message):
            
            username = message.from_user.username
            
            if username in admin_username: # If the desired username was in the admin list, we give the user access to administrative commands
                
                keyboard = [
                    [InlineKeyboardButton("دریافت اطلاعات مشتریان", callback_data='get_user_info'),
                    InlineKeyboardButton("ارسال پیام دسته جمعی" , callback_data='send_msg')]
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


        # از اینجا به بعد

        @bot.on_callback_query(filters.regex('^send_msg$'))
        async def send_customer_message(client, callback_query):
            try:
                phone = "+989160855428"
                client = TelegramClient('find_chat_id', api_id, api_hash)
                await client.connect()       

                if not await client.is_user_authorized():
                    print(12)
                    await client.send_code_request(phone)
                    code = input('Enter the Telegram code: ')
                    try:
                        await client.sign_in(phone, code)
                    except SessionPasswordNeededError:
                        password = getpass.getpass('Enter the password for the Telegram session ')
                        await client.sign_in(password=password)
                Chat_IDs = []
                unavailable_numbers = []
                available_numbers = []
                targets = 'targets.xlsx'

                df = pd.read_excel(targets , usecols= ['phone_number'])
                phone_numbers = df.values
        
                for phone_number in phone_numbers:
                    contact = InputPhoneContact(client_id=0, phone=f'{phone_number}', first_name='Contacto', last_name='Temporal')
                    result = await client(ImportContactsRequest([contact]))
                    if result.users:
                        user = result.users[0]
                        user_id = user.id
                        Chat_IDs.append(user_id)
                        available_numbers.append(phone_number)

                        await client.send_message(user_id , "سلام. این یک پیام تست است")
                        print(f"پیام ارسال شدبه {phone_number}")
                    
                        await client(DeleteContactsRequest(id=[InputUser(user_id=user.id, access_hash=user.access_hash)]))
                    else:
                        unavailable_numbers.append(phone_number)
                await callback_query.message.reply_text(f"اتمام عملیات")
                
            
            
            


            except Exception as e:
                await callback_query.message.reply_text(f"خطایی رخ داد: {e}")


        bot.run()
