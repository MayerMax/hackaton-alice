from __future__ import unicode_literals

import json
import logging


from flask import Flask, request
app = Flask(__name__)

from application.activity  import SimpleLevel, HardLevel


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
userStateStorage = {}
userLevelStorage = {}

#все доступные слова
words_base = ['а', 'б']

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def start_game(req, res):
    user_id = req['session']['user_id']
    sessionStorage[user_id] = {
        'suggests': [
            "простой",
            "сложный"
        ]
    }
    res['response']['text'] = 'Привет! Давай я загадаю тебе слово, ты попробуешь его отгадать. Выбери уровень!'
    res['response']['buttons'] = get_suggests(user_id)


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        start_game(req, res)
        userStateStorage[user_id] = 0
        return
    state, action = states[userStateStorage[user_id]]
    action(req, res)
    # # Обрабатываем ответ пользователя.
    # if req['request']['original_utterance'].lower() in [
    #     'ладно',
    #     'куплю',
    #     'покупаю',
    #     'хорошо',
    # ]:
    #     # Пользователь согласился, прощаемся.
    #     res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
    #     return
    #
    # # Если нет, то убеждаем его купить слона!
    # res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
    #     req['request']['original_utterance']
    # )
    # res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]
    return [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

def generate_word():
    return '4п'


def choose_level(req, res):
    user_id = req['session']['user_id']
    chosen_level = req['request']['original_utterance'].lower()
    if chosen_level in sessionStorage[user_id]['suggests']:
        userStateStorage[user_id] += 1
        word = generate_word()
        userLevelStorage[user_id] = SimpleLevel(word) if 'простой' else HardLevel(word)
        res['response']['text'] =  userLevelStorage[user_id].get_instruction()
    else:
        res['response']['text'] = 'Такого уровня нет, выбери простой или сложный'


def make_move(req, res):
    user_id = req['session']['user_id']
    level = userLevelStorage[user_id]
    input = req['request']['original_utterance'].lower()
    if level.is_correct_input(input):
        if level.is_completed():
            res['response']['text'] = 'Молодец, угадал! Сыграем еще раз?'
            userStateStorage[user_id] += 1
            return
            # TODO: кнопки для начала игры снова
        else:
            res['response']['text'] = level.get_instruction()
    else:
        res['response']['text'] = 'Неверно, давай еще раз.\n{}'.format(level.get_instruction())

def next_round(req, res):
    user_id = req['session']['user_id']
    answer = req['request']['original_utterance'].lower()
    if answer in ['да', 'давай', 'поехали', 'го', 'ладно']:
        level = userLevelStorage[user_id]
        level.restart(generate_word())
        userStateStorage[user_id] -= 1
        res['response']['text'] = 'Cлушай внимательно!\n{}'.format(level.get_instruction())
    elif answer in ['нет', 'не хочу', 'не буду']:
        res['response']['text'] = 'Спасибо за игру! Если захочешь сыграть еще раз, скажи мне какой уровень сложности выбрать и начнем сначала.'
        userStateStorage[user_id] = 0
    else:
        res['response']['text'] = 'Сыграешь?'


#состояния
states = [('level', choose_level),
          ('play', make_move),
          ('next round', next_round)]


if __name__ == '__main__':
    app.run()