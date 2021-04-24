import json
from random import randint
import sqlite3

from flask import Flask, request

from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

privetctvia = ['О ты ещё живой', 'Привет старый', 'Я думал ты опять сидишь в тюрьме)']
ID_USERS = str()
TOKENS = 0
ANSWER = str()


@app.route('/post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    global privetctvia, TOKENS, ID_USERS

    if req['session']['new']:
        con = sqlite3.connect('DB_Ded_Makar.db')
        cur = con.cursor()
        result = cur.execute("""SELECT id, tokens FROM users""").fetchall()
        for i in result:
            if req['session']['user_id'] == i[0]:
                TOKENS = i[1]
                ID_USERS = i[0]

                res['response']['text'] = 'На связи Макарыч!'
                res['response']['buttons'] = [
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia)) - 1),
                        'hide': True
                    },
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia) - 1)),
                        'hide': True
                    },
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia) - 1)),
                        'hide': True
                    }
                ]
                return
            else:
                con = sqlite3.connect('DB_Ded_Makar.db')
                cur = con.cursor()
                cur.execute(f"""INSERT INTO users(id, tokens) VALUES(?, ?)""",
                            (req['session']['user_id'], 1000)).fetchall()
                con.commit()
                con.close()
                res['response']['text'] = 'О свежее мясо круто! Я Макарыч, помогу скоротать твои ' \
                                          'скучные одинокие вечера. За всё в этой жизни надо платить и я ' \
                                          'просто так ничего не делаю. Возможность зарабатывать тугрики я тебе дам,' \
                                          'так что не боись. А ещё одно, так как я очень добрый то на первоначальные ' \
                                          'расходы дам тебе 1000☸. Все давай плыви в это море отсылок.'
                res['response']['buttons'] = [
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia)) - 1),
                        'hide': True
                    },
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia) - 1)),
                        'hide': True
                    },
                    {
                        'title': privetctvia.pop(randint(0, len(privetctvia) - 1)),
                        'hide': True
                    }
                ]
                return
        con.close()

    if 'привет старый' or 'о ты ещё живой' or 'я думал ты опять сидишь в тюрьме)' \
            in req['request']['original_utterance']:
        if 'Есть ещё что-нибудь на примете?' in req['request']['original_utterance']:
            film(req, res)
        elif 'Посоветуй ещё что-нибудь!' in req['request']['original_utterance']:
            sovet(req, res)
        elif 'ХВХАХВХАХВАХВ ЕЕЕЕЕЩЩЩЩЁЁЁЁЁЁЁ' in req['request']['original_utterance']:
            anecdot(req, res)
        elif 'Макарыч, я пошел, пока!' in req['request']['original_utterance']:
            prochanie(req, res)
        elif 'Заработать Макар-токенов.' in req['request']['original_utterance']:
            zarabotok(req, res)
        elif 'Бросить кубик.' in req['request']['original_utterance']:
            brosok_kybika(req, res)
        elif 'Ничего не понял, но очень интересно.' in req['request']['original_utterance']:
            randomna_figny(req, res)
        elif 'H6QT08NIG' in req['request']['original_utterance']:
            con = sqlite3.connect('DB_Ded_Makar.db')
            cur = con.cursor()
            result = cur.execute("""SELECT anecdot FROM tablisa_so_vsem""").fetchall()
            anecdot1 = result[randint(0, len(result) - 1)][0]
            while anecdot1 == None:
                anecdot1 = result[randint(0, len(result) - 1)][0]
            res['response']['text'] = anecdot1
            knopki(req, res)
        elif 'SOVET_POGOGDA' in req['request']['original_utterance']:
            con = sqlite3.connect('DB_Ded_Makar.db')
            cur = con.cursor()
            result = cur.execute("""SELECT sovet FROM tablisa_so_vsem""").fetchall()
            sovet1 = result[randint(0, len(result) - 1)][0]
            while sovet1 == None:
                sovet1 = result[randint(0, len(result) - 1)][0]
            res['response']['text'] = sovet1
            knopki(req, res)
        elif 'ABOBA' in req['request']['original_utterance']:
            res['response']['text'] = 'ABOBA'
            knopki(req, res)
        elif 'Создатели и творцы' in req['request']['original_utterance']:
            res['response']['text'] = 'Гении'
            knopki(req, res)
        elif 'Яндекс.Лицей' in req['request']['original_utterance']:
            res['response']['text'] = 'ПРЕКРАСНОЕ МЕСТО ДЛЯ РАЗВИТИЯ УМА И МЫСЛИТЕЛЬНЫХ ПРОЦЕССОВ'
            knopki(req, res)
        else:
            res['response']['text'] = f'Блатной если ты не забыл у тебя {TOKENS}☸. Трать их с умом или вали отсюда.'
            knopki(req, res)

            if 'Посоветуй фильм, Макарыч : 30☸' in req['request']['original_utterance']:
                film(req, res)
            elif 'Дай мне совет, отче: 20☸' in req['request']['original_utterance']:
                sovet(req, res)
            elif 'Хочу посмеяться: 10☸' in req['request']['original_utterance']:
                anecdot(req, res)
            elif 'Макарыч, я пошел, пока!' in req['request']['original_utterance']:
                prochanie(req, res)
            elif 'Заработать Макар-токенов ☸.' in req['request']['original_utterance']:
                zarabotok(req, res)
            elif 'Рандомная фигня.' in req['request']['original_utterance']:
                randomna_figny(req, res)


def film(req, res):
    global TOKENS
    if TOKENS >= 30:
        con = sqlite3.connect('DB_Ded_Makar.db')
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET tokens=? WHERE id=?""", (TOKENS, ID_USERS)).fetchall()
        TOKENS -= 30
        result = cur.execute("""SELECT film, fotka FROM tablisa_so_vsem""").fetchall()
        filmes = result[randint(0, len(result) - 1)]
        while filmes[0] == None:
            filmes = result[randint(0, len(result) - 1)]
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['description'] = filmes[0]
        res['response']['card']['image_id'] = filmes[1]
        res['response']['text'] = '1'
        res['response']['buttons'] = [
            {
                'title': 'Есть ещё что-нибудь на примете?',
                'hide': True
            },
            {
                'title': 'Спасибо за помощь, Макарыч!',
                'hide': True
            }
        ]
        con.commit()
        con.close()
    else:
        res['response']['text'] = 'Мало деняг нужно больше деняг'
        res['response']['buttons'] = [
            {
                'title': 'Заработать Макар-токенов ☸.',
                'hide': True
            },
            {
                'title': 'Макарыч, я пошел, пока!',
                'hide': True
            }
        ]
        return


def sovet(req, res):
    global TOKENS
    if TOKENS >= 20:
        con = sqlite3.connect('DB_Ded_Makar.db')
        cur = con.cursor()
        result = cur.execute("""SELECT sovet FROM tablisa_so_vsem""").fetchall()
        TOKENS -= 20
        cur.execute(f"""UPDATE users SET tokens=? WHERE id=?""", (TOKENS, ID_USERS)).fetchall()
        sovetik = result[randint(0, len(result) - 1)][0]
        while sovetik == None:
            sovetik = result[randint(0, len(result) - 1)][0]
        res['response']['text'] = sovetik
        res['response']['buttons'] = [
            {
                'title': 'Посоветуй ещё что-нибудь!',
                'hide': True
            },
            {
                'title': 'Пока с меня хватит этих гениальных советов.',
                'hide': True
            }
        ]
        con.commit()
        con.close()
    else:
        res['response']['text'] = 'Я похож на того кто будет что-то делать просто так???'
        res['response']['buttons'] = [
            {
                'title': 'Заработать Макар-токенов ☸.',
                'hide': True
            },
            {
                'title': 'Макарыч, я пошел, пока!',
                'hide': True
            }
        ]
        return


def anecdot(req, res):
    global TOKENS
    if TOKENS >= 10:
        global memy
        con = sqlite3.connect('DB_Ded_Makar.db')
        cur = con.cursor()
        result = cur.execute("""SELECT anecdot FROM tablisa_so_vsem""").fetchall()
        TOKENS -= 10
        cur.execute(f"""UPDATE users SET tokens=? WHERE id=?""", (TOKENS, ID_USERS)).fetchall()
        mem = result[randint(0, len(result) - 1)][0]
        while mem == None:
            mem = result[randint(0, len(result) - 1)][0]
        res['response']['text'] = mem
        res['response']['buttons'] = [
            {
                'title': 'ХВХАХВХАХВАХВ ЕЕЕЕЕЩЩЩЩЁЁЁЁЁЁЁ',
                'hide': True
            },
            {
                'title': 'Так это уже не смешно.',
                'hide': True
            }
        ]
        con.commit()
        con.close()
    else:
        res['response']['text'] = 'Даже мои шутки чего-то да стоят.'
        res['response']['buttons'] = [
            {
                'title': 'Заработать Макар-токенов ☸.',
                'hide': True
            },
            {
                'title': 'Макарыч, я пошел, пока!',
                'hide': True
            }
        ]
        return


def zarabotok(req, res):
    res['response'][
        'text'] = 'Бросим кости, так как я добрый и ленивый, то если у нас будет ничья или ты победишь ' \
                  'получишь 10 ☸,а если выиграю я то скажу что ты зафаршмачился.'
    res['response']['buttons'] = [
        {
            'title': 'Бросить кубик.',
            'hide': True
        }
    ]
    return


def brosok_kybika(req, res):
    global TOKENS
    ded, moe = randint(1, 6), randint(1, 6)
    if ded > moe:
        res['response']['text'] = f'Ты зафаршмачился у меня {ded}, а у тебя {moe}'
    else:
        res['response']['text'] = f'Твоя взяла, у меня {ded}, а у тебя {moe}, но особо не радуйся фраей.'
        con = sqlite3.connect('DB_Ded_Makar.db')
        cur = con.cursor()
        result = cur.execute("""SELECT sovet FROM tablisa_so_vsem""").fetchall()
        TOKENS += 10
        cur.execute(f"""UPDATE users SET tokens=? WHERE id=?""", (TOKENS, ID_USERS)).fetchall()
        con.commit()
        con.close()
    res['response']['buttons'] = [
        {
            'title': 'Бросить кубик.',
            'hide': True
        },
        {
            'title': 'Пока хватит игр.',
            'hide': True
        }
    ]
    return


def randomna_figny(req, res):
    con = sqlite3.connect('DB_Ded_Makar.db')
    cur = con.cursor()
    result = cur.execute("""SELECT figna FROM tablisa_so_vsem""").fetchall()
    fig = result[randint(0, len(result) - 1)][0]
    while fig == None:
        fig = result[randint(0, len(result) - 1)][0]
    res['response']['text'] = fig
    res['response']['buttons'] = [
        {
            'title': 'Ничего не понял, но очень интересно.',
            'hide': True
        },
        {
            'title': 'Оставляю тебя с твоей шизой Макарыч.',
            'hide': True
        }
    ]
    con.close()


def prochanie(req, res):
    res['response']['end_session'] = True
    res['response']['text'] = 'Давай фраер, удачи тебе.'


def knopki(req, res):
    res['response']['buttons'] = [
        {
            'title': 'Посоветуй фильм, Макарыч : 30☸',
            'hide': True
        },
        {
            'title': 'Дай мне совет, отче: 20☸',
            'hide': True
        },
        {
            'title': 'Хочу посмеяться: 10☸',
            'hide': True
        },
        {
            'title': 'Заработать Макар-токенов ☸.',
            'hide': True
        },
        {
            'title': 'Рандомная фигня.',
            'hide': True
        },
        {
            'title': 'Макарыч, я пошел, пока!',
            'hide': True
        }
    ]


if __name__ == '__main__':
    app.run()
