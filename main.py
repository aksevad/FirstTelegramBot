"""
bot for antennas pointing
"""

import telebot
import logging
import psycopg2

from resources.phrases import phrases
from config import BOT_TOKEN, DB_URL
from antennaclass import SatelliteAntenna

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URL, sslmode="require")
db_object = db_connection.cursor()


@bot.message_handler(commands=['start', 'location', 'eng', 'ru', 'rst', 'reset', 'about', 'help'])
def start(message):
    # global language
    # global process_step
    global cases
    chat_id = message.chat.id
    user_id = message.from_user.id
    smg = message.text.lower()
    try:
        language = cases.get(chat_id).get_language()
    except:
        language = "ENG"
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    if smg == '/start':
        # process_step = 1
        #sql_input_to_chat(chat_id, user_id)

        cases.update({chat_id: SatelliteAntenna(language=language)})
        # cases.get(chat_id).set_process_step(1)

        # print(cases.get(chat_id).get_sat_longitude().__str__())
        bot.send_message(message.chat.id, phrases['bot_entrance'][language] + f" {message.from_user.first_name}",
                         parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['language_select'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['process_started'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['sat_long_request'][language], parse_mode='HTML')
    elif smg == '/location':
        bot.send_message(message.chat.id, "Ura", parse_mode='HTML')
    elif smg == '/eng':
        language = "ENG"
        if not cases.get(chat_id):
            cases.update({chat_id: SatelliteAntenna(language=language)})
        else:
            cases.get(chat_id).set_language(language)
        bot.send_message(message.chat.id, phrases['change_language'][language], parse_mode='HTML')
    elif smg == '/ru':
        language = "RU"
        if not cases.get(chat_id):
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            cases.update({chat_id: SatelliteAntenna(language=language)})
            #print(cases.get(chat_id).get_language())
        else:
            cases.get(chat_id).set_language(language)
        bot.send_message(message.chat.id, phrases['change_language'][language], parse_mode='HTML')
    elif smg == '/rst' or smg == '/reset':
        bot.send_message(message.chat.id, phrases['reset_requested'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['process_started'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['sat_long_request'][language], parse_mode='HTML')
        # process_step = 1
        #sql_input_to_chat(chat_id, user_id)
        cases.update({chat_id: SatelliteAntenna(language=language)})

    elif smg == '/about':
        bot.send_message(message.chat.id, phrases['disclaimer'][language], parse_mode='HTML')
    elif smg == '/help':
        bot.send_message(message.chat.id, phrases['help'][language], parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, phrases['unknown_command'][language], parse_mode='HTML')


@bot.message_handler()
def get_user_text(message):
    # global antenna
    # global process_step
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        process_step = cases.get(chat_id).get_process_step()
    except:
        process_step = 0
    try:
        language = cases.get(chat_id).get_language()
    except:
        language = "ENG"

    if message.text == 'photo':
        photo = open("./resources/satellite.png", 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == '??full_info??':
        bot.send_message(message.chat.id, message, parse_mode='HTML')
    else:
        # collecting data from user through dialog
        if process_step == 1:
            # satellite longitude
            if cases.get(chat_id).set_sat_longitude(message.text):
                # success. go to next step
                process_step = 2
                #sql_input_to_chat(chat_id, user_id, sat_longitude=cases.get(chat_id).get_sat_longitude())
                bot.send_message(message.chat.id, phrases['sat_long_achieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['antenna_location_request'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
        elif process_step == 2:
            # antenna coordinates
            if cases.get(chat_id).set_antenna_coordinates_str(message.text):
                # success. go to next step
                process_step = 3
                #sql_input_to_chat(chat_id, user_id)
                bot.send_message(message.chat.id, phrases['antenna_location_achieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['antenna_offset_request'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
        elif process_step == 3:
            # timezone
            if cases.get(chat_id).set_antenna_offset_str(message.text):
                # success. go to next step
                process_step = 4
                #sql_input_to_chat(chat_id, user_id)
                bot.send_message(message.chat.id, phrases['antenna_offset_ahcieved'][language], parse_mode='HTML')
                bot.send_message(message.chat.id, phrases['calculations_1'][language], parse_mode='HTML')
            else:
                # wrong data in message
                bot.send_message(message.chat.id, phrases['wrong_input'][language], parse_mode='HTML')
            # final calculations
            cases.get(chat_id).set_now()
            # antenna.set_antenna_coordinates_str("63,3N;75.53E")
            # antenna.set_sat_longitude("-66")
            # ofangle = 17  #ofset angel of antenna
            twilightr = -7
            # antenna.set_antenna_offset(ofangle)
            results = cases.get(chat_id).sunpos(twilightr)
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

        cases.get(chat_id).set_process_step(process_step)


# @bot.message_handler(commands=['location'])
# def geolocation(message):
#     bot.send_message(message.chat.id, message, parse_mode='HTML')

# def sql_input_to_chat(chat_id, user_id, sat_longitude=0):
#     # global language
#     # global process_step
#     global cases
#     db_object.execute(f"SELECT chat_id FROM chats WHERE chat_id = {chat_id}")
#     result = db_object.fetchone()
#
#     if not result:
#         db_object.execute(
#             "INSERT INTO chats(chat_id, user_id, current_step, user_language, satellite_longitude) VALUES(%s, %s, %s, %s, %s)",
#             (chat_id, user_id, cases.get(chat_id).get_process_step(), cases.get(chat_id).get_language(), sat_longitude))
#         db_connection.commit()
#         logger.debug("new record in DB (chats)")
#     else:
#         db_object.execute(
#             "UPDATE chats SET current_step = %s, user_language = %s, satellite_longitude= %s WHERE chat_id = %s",
#             (cases.get(chat_id).get_process_step(), cases.get(chat_id).get_language(), sat_longitude, chat_id))
#         db_connection.commit()
#         logger.debug("update record in DB (chats)")
#     return True


if __name__ == '__main__':
    # global language
    # global process_step
    # global antenna

    global cases

    # antenna = SatelliteAntenna()

    # language = "ENG"
    # process_step = 0
    cases = {"0": SatelliteAntenna()}
    bot.polling(none_stop=True)
