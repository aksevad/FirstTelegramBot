"""
preloaded phrases for bot dialogs
"""

languages = {"ENG": 0, "RU": 1, "DE": 2}

phrases = {
    "bot_entrance": {"ENG": "Hello", "RU": "Привет"},
    "help": {"ENG": "help", "RU": "help"},
    "change_language": {"ENG": "Switched to English", "RU": "Переключился на Русский"},
    "unknown_command": {"ENG": "Unknown command", "RU": "Нет такой команды"},
    "unknown_text": {"ENG": "I can`t understand You", "RU": "Я тебя не понимаю"},
    "reset_requested": {"ENG": "Let`s start from the begin", "RU": "Начинаем заново"},
    "wrong_input": {"ENG": "Wrong input. Try one more time", "RU": "Введено некоректно. Повтори"},
    "sat_long_request": {"ENG": "...",
                         "RU": "Введи долготу спутника в формате от -180->180 (где отрицательные числа для восточного полушария), или 0E->180E и 0W->180W (где E - восточное и W - западное полушарие)"},
    "sat_long_achieved": {"ENG": "...", "RU": "Долгота спутника сохранена."},
    "antenna_location_request": {"ENG": "...",
                                 "RU": "Координаты антенны в одном из форматов:\n "
                                       "-90.0000 -> 90.0000;-180.0000 -> 180.0000 (где - для Южного и Восточного полушариев соответственно)\n"
                                       "0.0000S/N -> 90.0000S/N;0.0000E/W -> 180.0000E/W (где S, N, E, W - южное, северное, восточное, западное полушария соответственно)"},
    "antenna_location_achieved": {"ENG": "...", "RU": "Координаты антенны получены."},
    #"timezone_request": {"ENG": "...", "RU": "временной пояс."},
    #"timezone_achieved": {"ENG": "...", "RU": "временной пояс получен."},
    "antenna_offset_request": {"ENG": "...", "RU": "Введи офсетный угол антенны в градусах в формате 0.0 -> 90.0"},
    "antenna_offset_ahcieved": {"ENG": "...", "RU": "Офсетный угол антенны принят"},
    "calculations_1": {"ENG": "...", "RU": "начал расчеты."},
    "calculations_2": {"ENG": "...", "RU": "начал расчеты 2."},
    "result_success": {"ENG": "...", "RU": "результат получен."},
    "result_failed": {"ENG": "...", "RU": "результат не получен."},
    "dialog_finish": {"ENG": "...", "RU": "работа завершена. старт для новых расчетов."},
    "process_started": {
        "ENG": "Go through the dialog step by step. Write \"\\rst\" or \"\\reset\" if something is going wrong",
        "RU": "Следуй диалогу пошагово. Напиши \"\\rst\" или \"\\reset\" если что-то пошло не так"},
    "disclaimer": {
        "ENG": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>",
        "RU": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>"},
}

