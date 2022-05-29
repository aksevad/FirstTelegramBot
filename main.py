"""
bot for antennas pointing
"""

import telebot
import logging
import psycopg2

from resources.phrases import phrases, success_result_dialog
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

    if smg == '/start':
        # process_step = 1
        # sql_input_to_chat(chat_id, user_id)

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
            cases.update({chat_id: SatelliteAntenna(language=language)})
        else:
            cases.get(chat_id).set_language(language)
        bot.send_message(message.chat.id, phrases['change_language'][language], parse_mode='HTML')
    elif smg == '/rst' or smg == '/reset':
        bot.send_message(message.chat.id, phrases['reset_requested'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['process_started'][language], parse_mode='HTML')
        bot.send_message(message.chat.id, phrases['sat_long_request'][language], parse_mode='HTML')
        # process_step = 1
        # sql_input_to_chat(chat_id, user_id)
        cases.update({chat_id: SatelliteAntenna(language=language)})

    elif smg == '/about':
        bot.send_message(message.chat.id, phrases['disclaimer'][language], parse_mode='HTML')
    elif smg == '/help':
        bot.send_message(message.chat.id, phrases['help'][language], parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, phrases['unknown_command'][language], parse_mode='HTML')


@bot.message_handler()
def get_user_text(message):
    global cases
    # global antenna
    # global process_step
    chat_id = message.chat.id
    # user_id = message.from_user.id

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
                # sql_input_to_chat(chat_id, user_id, sat_longitude=cases.get(chat_id).get_sat_longitude())
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
                # sql_input_to_chat(chat_id, user_id)
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
                # sql_input_to_chat(chat_id, user_id)
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
            result_output(message, language)
            sql_output(chat_id)
        else:
            bot.send_message(message.chat.id, phrases['unknown_text'][language], parse_mode='HTML')

    cases.get(chat_id).set_process_step(process_step)


def result_output(message, language):
    global cases
    chat_id = message.chat.id
    success_result_dialog_d = {'result_success': None,
                               'datetime': cases.get(chat_id).get_date_str(),
                               'sat_azimuth': cases.get(chat_id).get_satellite_azimuth(),
                               'sat_vertical_true': cases.get(chat_id).get_vertical(),
                               'sat_vertical_actual': cases.get(chat_id).get_vertical() - cases.get(
                                   chat_id).get_antenna_offset()
                               }

    if cases.get(chat_id).get_outcome() == 'SUCCESS':
        for line in success_result_dialog:
            # print(success_result_dialog_d[line])
            if isinstance(success_result_dialog_d[line], str):
                temp_str = phrases[line][language] + success_result_dialog_d[line]
            elif isinstance(success_result_dialog_d[line], None):
                temp_str = phrases[line][language]
            else:
                try:
                    temp_str = phrases[line][language] + success_result_dialog_d[line].__str__()
                except:
                    temp_str = phrases[line][language]

            bot.send_message(chat_id, temp_str, parse_mode='HTML')

    elif cases.get(chat_id).get_outcome() == 'OUT OF HORIZONT':
        bot.send_message(chat_id, phrases['out_of_horizont'][language], parse_mode='HTML')
    else:
        bot.send_message(chat_id, phrases['result_failed'][language], parse_mode='HTML')

    # if results[0] == "True":
    #     bot.send_message(chat_id, phrases['result_success'][language], parse_mode='HTML')
    #     for result in results:
    #         if result != "True":
    #             bot.send_message(chat_id, result, parse_mode='HTML')
    #
    # else:
    #     bot.send_message(message.chat.id, phrases['result_failed'][language], parse_mode='HTML')
    bot.send_message(message.chat.id, phrases['dialog_finish'][language], parse_mode='HTML')


def sql_output(chat_id):
    global cases
    db_object.execute("SELECT MAX(id) FROM calculations")
    haul = db_object.fetchone()
    try:
        id = int(haul[0])
    except:
        id = 0
    id = id + 1
    # print(result)
    # print("ID=%s", (id.__str__()))
    parities = cases.get(chat_id).get_sun_sat_parity_time()
    db_object.execute(
        "INSERT INTO calculations(id, calculation_date_utc, calculation_time_utc, antenna_latitude, "
        "antenna_longitude, antenna_offset, satellite_longitude, calculated_satellite_azimuth, "
        "calculated_sun_azimuth, calculated_true_vertical, calculated_sun_satellite_m45_parity, "
        "calculated_sun_satellite_m30_parity, calculated_sun_satellite_parity, "
        "calculated_sun_satellite_p30_parity, calculated_sun_satellite_p45_parity, result)"
        " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (id, cases.get(chat_id).get_date_str(), cases.get(chat_id).get_time_str(),
         cases.get(chat_id).get_antenna_latitude(), cases.get(chat_id).get_antenna_longitude(),
         cases.get(chat_id).get_antenna_offset(), cases.get(chat_id).get_sat_longitude(),
         cases.get(chat_id).get_satellite_azimuth(), cases.get(chat_id).get_sun_azimuth(),
         cases.get(chat_id).get_vertical(), parities['m45'], parities['m30'], parities['mp0'],
         parities['p30'], parities['p45'], cases.get(chat_id).get_outcome()))
    db_connection.commit()
    logger.debug("new record in DB (calculations)")


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
