"""
bot for antennas pointing
"""

import telebot
import logging

from resources.phrases import phrases
from config import BOT_TOKEN
from antennaclass import SatelliteAntenna

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start', 'location', 'eng', 'ru', 'rst', 'reset', 'about', 'help'])
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
    elif smg == '/help':
        bot.send_message(message.chat.id, phrases['help'][language], parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, phrases['unknown_command'][language], parse_mode='HTML')


@bot.message_handler()
def get_user_text(message):
    global antenna
    global process_step
    if message.text == 'photo':
        photo = open("./resources/satellite.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == '__full_info__':
        bot.send_message(message.chat.id, message, parse_mode='HTML')
    else:
        # collecting data from user through dialog
        if process_step == 1:
            # satellite longitude
            if antenna.set_sat_longitude(message.text):
                # success. go to next step
                process_step = 2
                bot.send_message(message.chat.id, phrases['sat_long_achieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['antenna_location_request'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
        elif process_step == 2:
            # antenna coordinates
            if antenna.set_antenna_coordinates_str(message.text):
                # success. go to next step
                process_step = 3
                bot.send_message(message.chat.id, phrases['antenna_location_achieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['antenna_offset_request'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
        elif process_step == 3:
            # timezone
            if antenna.set_antenna_offset_str(message.text):
                # success. go to next step
                process_step = 4
                bot.send_message(message.chat.id, phrases['antenna_offset_ahcieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['calculations_1'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
            # final calculations
            antenna.set_now()
            # antenna.set_antenna_coordinates_str("63,3N;75.53E")
            # antenna.set_sat_longitude("-66")
            # ofangle = 17  #ofset angel of antenna
            twilightr = -7
            # antenna.set_antenna_offset(ofangle)
            results = antenna.sunpos(twilightr)
            if results[0] == "True":
                bot.send_message(message.chat.id, phrases['result_success'][language], parse_mode='HTML')
                for result in results:
                    if result != "True":
                        bot.send_message(message.chat.id, result, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, phrases['result_failed'][language], parse_mode='HTML')
            # bot.send_message(message.chat.id, phrases['calculations_2'][language], parse_mode='HTML')
            bot.send_message(message.chat.id, phrases['dialog_finish'][language], parse_mode='HTML')

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
