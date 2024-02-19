import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace 'YOUR_BOT_TOKEN' with the token provided by BotFather
bot_token = 'YOUR_BOT_TOKEN'

# Initialize the bot
bot = telebot.TeleBot(bot_token)

user_states = {}
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Bot is Connected.')

@bot.message_handler(commands=['download'])
def download(message):
    user_id = message.chat.id
    user_states[user_id] = {'step':1,'url':None,'file_name':None}
    bot.send_message(user_id,'Give me the direct download link of the file \nExample:   https://download.com/pic.jpg')

@bot.message_handler(func=lambda message:user_states.get(message.chat.id) and user_states[message.chat.id]['step'] == 1)
def get_url(message):
    user_id = message.chat.id
    user_states[user_id]['url'] = message.text
    user_states[user_id]['step'] = 2
    bot.send_message(user_id,f'Thanks for the link ({message.text}) \nSend me the (file name [with extension]) \n\nExample:   pic.jpg',disable_web_page_preview=True)

@bot.message_handler(func=lambda message:user_states.get(message.chat.id) and user_states[message.chat.id]['step'] == 2)
def get_file_name(message):
    user_id = message.chat.id
    user_states[user_id]['file_name'] = message.text
    url = user_states[user_id]['url']
    file_name = user_states[user_id]['file_name']
    
    data = f''''Your Data :
    Download Link: {url}
    
    File Name: {file_name}
    
    Downloding........'''

    bot.send_message(user_id,data,disable_web_page_preview=True)
    
    
    res = requests.get(url).content
    with open(file_name,'wb')as f:
        f.write(res)
    bot.send_photo(user_id,photo=res,caption=f"File Name: {file_name}")
    

    




# Start the bot
try:
    bot.polling()
except:
    pass
# bot = telebot.TeleBot('')

'''
# Function to handle the /start command
@bot.message_handler(commands=['download'])
def start(message):
    chat_id = message.chat.id
    message_text = "Choose an option:"

    # Create inline buttons
    inline_markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Button 1", callback_data='jpg')
    button2 = InlineKeyboardButton("Button 1", callback_data='png')
    
    inline_markup.row(button1, button2)

    bot.send_message(chat_id, message_text, reply_markup=inline_markup)

# Function to handle inline button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    chat_id = call.message.chat.id
    button_data = call.data

    if button_data == 'button1':
        reply_message = "You clicked Button 1"
    elif button_data == 'button2':
        reply_message = "You clicked Button 2"
    else:
        reply_message = "Unknown button"

    bot.answer_callback_query(call.id)
    bot.send_message(chat_id, reply_message)'''
