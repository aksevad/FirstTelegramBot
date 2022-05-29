"""
preloaded phrases for bot dialogs
"""

languages = {"ENG": 0, "RU": 1, "DE": 2}

success_result_dialog = ['result_success', 'datetime', 'sat_azimuth', 'sat_vertical_true', 'sat_vertical_actual']

phrases = {
    "bot_entrance": {"ENG": "Hello", "RU": "Привет"},
    "help": {"ENG": "help function does not exist yet", "RU": "раздел помощи еще не создан"},
    "change_language": {"ENG": "Switched to English", "RU": "Переключился на Русский"},
    "language_select": {"ENG": "<b>/eng</b> for English \n<b>/ru</b> для Русского",
                        "RU": "<b>/eng</b> for English \n<b>/ru</b> для Русского"},
    "unknown_command": {"ENG": "Unknown command", "RU": "Нет такой команды"},
    "unknown_text": {"ENG": "I can`t understand You", "RU": "Я тебя не понимаю"},
    "reset_requested": {"ENG": "Let`s start from the begin", "RU": "Начинаем заново"},
    "wrong_input": {"ENG": "Wrong input. Try one more time", "RU": "Введено некоректно. Повтори"},
    "sat_long_request": {
        "ENG": "Enter the longitude of the satellite in the format from -180->180 (where negative numbers are for the eastern hemisphere)"
               "or 0E->180E and 0W->180W (where E is East and W is West hemisphere)",
        "RU": "Введи долготу спутника в формате от -180->180 (где отрицательные числа для восточного полушария),"
              " или 0E->180E и 0W->180W (где E - восточное и W - западное полушарие)"},
    "sat_long_achieved": {"ENG": "Satellite longitude was saved", "RU": "Долгота спутника сохранена."},
    "antenna_location_request": {"ENG": "Input antenna coordinates in one of available formats:\n"
                                        "-90.0000 -> 90.0000;-180.0000 -> 180.0000 (where - for the Southern and Eastern hemispheres, respectively)\n"
                                        "0.0000S/N -> 90.0000S/N;0.0000E/W -> 180.0000E/W (where S, N, E, W are the southern, northern, eastern, western hemispheres, respectively)",
                                 "RU": "Введи координаты антенны в одном из форматов:\n "
                                       "-90.0000 -> 90.0000;-180.0000 -> 180.0000 (где - для Южного и Восточного полушариев соответственно)\n"
                                       "0.0000S/N -> 90.0000S/N;0.0000E/W -> 180.0000E/W (где S, N, E, W - южное, северное, восточное, западное полушария соответственно)"},
    "antenna_location_achieved": {"ENG": "Antenna coordinates were saved", "RU": "Координаты антенны получены."},
    "antenna_offset_request": {"ENG": "Input antenna offset angle in grads in range 0.0 -> 90.0",
                               "RU": "Введи офсетный угол антенны в градусах в формате 0.0 -> 90.0"},
    "antenna_offset_ahcieved": {"ENG": "Antenna offset angle was saved", "RU": "Офсетный угол антенны принят"},
    "calculations_1": {"ENG": "calculations", "RU": "начал расчеты."},
    "out_of_horizont": {"ENG": "the satellite is below horizont", "RU": "спутник ниже линии горизонта"},
    "calculations_2": {"ENG": "calculations", "RU": "начал расчеты 2."},
    "result_success": {"ENG": "success", "RU": "результат получен."},
    "result_failed": {"ENG": "UPS! failed.", "RU": "результат не получен."},
    "datetime": {"ENG": "Date & Time (GTM):", "RU": "Дата и Время (GTM):"},
    "sat_azimuth": {"ENG": "Satellite azimuth:", "RU": "Азимут спутника:"},
    "sat_vertical_true": {"ENG": "Vertical angle true:", "RU": "Угол места истиный:"},
    "sat_vertical_actual": {"ENG": "Vertical angle actual:", "RU": "Угол места актуальный:"},
    "sun_azimuth": {"ENG": "Sun azimuth:", "RU": "Азимут солнца:"},
    "dialog_finish": {"ENG": "job is done. <b>/start</b> for new calculation",
                      "RU": "работа завершена. <b>/start</b> для новых расчетов."},
    "process_started": {
        "ENG": "Go through the dialog step by step. Write <b>/rst</b> or <b>/reset</b> if something is going wrong",
        "RU": "Следуй диалогу пошагово. Напиши <b>/rst</b> или <b>/reset</b> если что-то пошло не так"},
    "disclaimer": {
        "ENG": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>",
        "RU": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>"},
}

# cikti = "Место: " + str(round(lao, 3)) + "° " + ("N" if self.__antenna_latitude > 0 else "S") + ",  " + \
#         str(round(lgo, 3)) + "° " + ("W" if self.__antenna_longitude < 0 else "E") + "\r"
# "timezone_request": {"ENG": "...", "RU": "временной пояс."},
# "timezone_achieved": {"ENG": "...", "RU": "временной пояс получен."},
