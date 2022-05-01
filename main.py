"""
bot for antennas pointing
"""

import telebot

from resources.phrases import phrases
from config import BOT_TOKEN
from antennaclass import SatelliteAntenna

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'location', 'eng', 'ru', 'rst', 'reset', 'about'])
def start(message):
    global language
    global process_step
    smg = message.text.lower()
    if smg == '/start':
        bot.send_message(message.chat.id, phrases['bot_entrance'][language] + f" {message.from_user.first_name}",
                         parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['process_started'][language], parse_mode='HTML')
        process_step = 1
        bot.send_message(message.chat.id, phrases['sat_long_request'][language], parse_mode='HTML')
    elif smg == '/location':
        bot.send_message(message.chat.id, "Ura", parse_mode='HTML')
    elif smg == '/eng':
        language = "ENG"
        bot.send_message(message.chat.id, phrases['change_language'][language], parse_mode='HTML')
    elif smg == '/ru':
        language = "RU"
        bot.send_message(message.chat.id, phrases['change_language'][language], parse_mode='HTML')
    elif smg == '/rst' or smg == '/reset':
        bot.send_message(message.chat.id, phrases['reset_requested'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['process_started'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['sat_long_request'][language], parse_mode='HTML')
        process_step = 1
    elif smg == '/about':
        bot.send_message(message.chat.id, phrases['disclaimer'][language], parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, phrases['unknown_command'][language], parse_mode='HTML')


@bot.message_handler()
def get_user_text(message):
    global antenna
    if message.text == 'photo':
        photo = open("./resources/satellite.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == '__full_info__':
        bot.send_message(message.chat.id, message, parse_mode='HTML')
    else:
        # collecting data from user through dialog
        if process_step == 1:
            # satellite longitude
            msg = message.text.lower().replace(" ", "").replace("w", "")
            if 'e' in msg:
                # Convert East to -
                msg = '-' + msg.replace("e", "")
            try:
                sat_longitude = int(float(msg).__round__(0))
                #print(sat_longitude)
            except Exception:
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
                return None
                print("1="+msg+"=")
            #print(type(sat_longitude))
            if -180 <= sat_longitude <= 180:
                antenna.set_sat_longitude(sat_longitude)
                bot.send_message(message.chat.id, "Lonitude is " + sat_longitude.__str__(), parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
                print("2="+msg+"=")
                return None
        else:
            bot.send_message(message.chat.id, phrases['unknown_text'][language], parse_mode='HTML')


# @bot.message_handler(commands=['location'])
# def geolocation(message):
#     bot.send_message(message.chat.id, message, parse_mode='HTML')

if __name__ == '__main__':
    global language
    global process_step
    global antenna

    antenna = SatelliteAntenna()

    language = "ENG"
    process_step = 0
    bot.polling(none_stop=True)
