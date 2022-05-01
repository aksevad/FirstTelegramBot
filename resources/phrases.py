"""
preloaded phrases for bot dialogs
"""

languages = {"ENG": 0, "RU": 1, "DE": 2}

phrases = {
    "bot_entrance": {"ENG": "Hello", "RU": "Привет"},
    "change_language": {"ENG": "Switched to English", "RU": "Переключился на Русский"},
    "unknown_command": {"ENG": "Unknown command", "RU": "Нет такой команды"},
    "unknown_text": {"ENG": "I can`t understand You", "RU": "Я тебя не понимаю"},
    "reset_requested": {"ENG": "Let`s start from the begin", "RU": "Начинаем заново"},
    "wrong_input": {"ENG": "Wrong input. Try one more time", "RU": "Введено некоректно. Повтори"},
    "sat_long_request": {"ENG": "...",
                         "RU": "Введи долготу спутника в формате от -180->180 (где отрицательные числа для восточного полушария), или 0E->180E и 0W->180W (где E - восточное и W - западное полушарие)"},
    "process_started": {
        "ENG": "Go through the dialog step by step. Write \"\\rst\" or \"\\reset\" if something is going wrong",
        "RU": "Следуй диалогу пошагово. Напиши \"\\rst\" или \"\\reset\" если что-то пошло не так"},
    "disclaimer": {
        "ENG": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>",
        "RU": "<a href=\"https://www.flaticon.com/free-icons/space-station\" title=\"space station icons\">Space station icons created by Assia Benkerroum  - Flaticon</a>"},
}

