import telegram 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import requests
import time
import urllib
#urllib helps to encode any special characters in our message eg. &/$
"""json module to parse JSON responses from Telegram into Python dictionaries
so that we can extract the pieces of data that we need"""
from dbhelper import DBHelper
db = DBHelper()

#long polling: server holds the request open until new data is available
TOKEN = "468631185:AAFSOHfNGZsI8YaGzkO2kU3pxidl563v-Q8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8") #decode for greater compatibility
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content) #telegram always gives JSON response
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_chat_id(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"] #message sent by user
        chat_id = update["message"]["chat"]["id"]
        if text == "/start": #starting the bot
            if db.check_for_user(chat_id):
                send_message("""Welcome back! You have taken the test before, would you want to retake the test?""")
                keyboard = yes_no_keyboard() #retype method
                send_message(keyboard)
            else:
                send_message("""Welcome to Myer Briggs Test Bot. The test consists of 70 MCQs,where you can either select A or B as your answer. The test will take approximately 30minutes to complete.
Send /hitmeup to begin the test.""", chat_id)
        elif text == "/hitmeup": #starting the test
            questions = db.getQuestions()
            for question in range(70):
                #display question
                send_message(questions[question][0], chat_id)
                #build keyboard
                #qn_keyboard = build_keyboard(question + 1)
                #display options
                #send_message("Choose an option", chat_id, qn_keyboard)
                qn_keyboard = option_keyboard(question + 1)
                send_message("Choose an option", chat_id, reply_markup=qn_keyboard)
        elif text.startswith("/"): #boolean checker
            continue
        else:
            send_message("""Sorry, we are unable to process what you just typed. Type /help for valid commands. Thank you!""")

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#reply_markup is an object that includes the keyboard along with other values
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def build_keyboard(question_number):
    #turns each item into a list, letting it be an entire row of the keyboard
    wanted_options = db.getOptions(question_number)
    keyboard = [[wanted_options[0][0]],[wanted_options[0][1]]]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    #converting the Python dictionary into a JSON string
    return json.dumps(reply_markup) 

def option_keyboard(question_number):
    wanted_options = db.getOptions(question_number)
    button_list = [InlineKeyboardButton(wanted_options[0][0], callback_data="a"),InlineKeyboardButton(wanted_options[0][1], callback_data="b")]
    reply_markup = InlineKeyboardMarkup(button_list)
    print(type(reply_markup))
    return reply_markup

def yes_no_keyboard():
    keyboard = ['yes','no']
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def main():
    db.setup()
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        #Checks /getUpdates API for new messages
        if len(updates["result"]) > 0:
            #Have to +1 because position 0 is oldest message
            last_update_id = get_last_update_id(updates) + 1
            updates = get_updates(last_update_id)
            print(updates)
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
