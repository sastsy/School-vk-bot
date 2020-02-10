import wikipedia
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import pyowm
import random


token = "bc20262f40e9cd8f296450b2c166361df06489fd3d8ef015c4213a25ce857b27d026e4e6841b70d896ada"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session, 189798950)

wikipedia.set_lang("RU")

idk_phrases = ['Прости, я не совсем тебя понимаю. Наверное, это потому что я не ходил в школу...',
               'Я твоя не понимать...', 'Пожалуйста, перефразируй.', 'Я понимаю только команды. Речь человека — загадка',
               'А ты умён!', 'Продолжай, мне очень интересно', 'Я не в настроении разговаривать',
               'Очень отсроумно', 'Из какого фильма эта фраза?', 'Задай мне другой вопрос', 'Зайцы!!']

owm = pyowm.OWM('1dcb7e23a20a50a66a560a3d5e35f515', language='ru')
temperature = owm.weather_at_place('Izhevsk, RU').get_weather().get_temperature('celsius')['temp']
temp_info1 = 'Похоже, что сейчас в Ижевске около ' + str(int(temperature)) + ' градусов. ' + 'Слишком холодно для занятий на улице!'
temp_info2 = 'Похоже, что сейчас в Ижевске около ' + str(int(temperature)) + ' градусов. ' + 'Погода подходит' \
             ' для занятий на улице, но обрати внимание на осадки, если они есть.'


keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Расписание звонков (40 минут)', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Расписание звонков (30 минут)', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Где физкультура?', color=VkKeyboardColor.DEFAULT)
keyboard.add_button('Википедия', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('График каникул', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Посчитать оценки', color=VkKeyboardColor.DEFAULT)
keyboard = keyboard.get_keyboard()


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text == 'Расписание звонков (40 минут)':
            session_api.messages.send(user_id=event.user_id, random_id='',
                                      keyboard=keyboard, attachment='photo-189798950_457239019')

        elif event.text == 'Расписание звонков (30 минут)':
            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard, attachment='photo-189798950_457239017')

        elif event.text == 'Где физкультура?':
            if temperature < -15:
                session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                          message=temp_info1)
            else:
                session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                          message=temp_info2)

        elif event.text == 'График каникул':
            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                      attachment='photo-189798950_457239018')

        elif event.text == 'Посчитать оценки':
            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                      message='Введите оценки в одну строку и через пробел.')
            for event_g in longpoll.listen():
                if event_g.type == VkEventType.MESSAGE_NEW and event_g.to_me:  # and ''.join(event_w.text.split()).isdigit():
                    numbers = event_g.text.split(' ')
                    checked = ''.join([str(i) for i in numbers])
                    if checked.isdigit():
                        five_to_five = 0
                        four_to_four = 0
                        five_to_four = 0
                        count = 0
                        n = 0
                        for i in numbers:
                            count += 1
                            n += int(i)
                        av = n / count
                        sred1 = av
                        sred2 = av
                        sred3 = av
                        while sred1 < 4.6:
                            five_to_five += 1
                            sred1 = (n + five_to_five * 5) / (count + five_to_five)
                        while sred2 < 3.6:
                            four_to_four += 1
                            sred2 = (n + four_to_four * 4) / (count + four_to_four)
                        while sred3 < 3.6:
                            five_to_four += 1
                            sred3 = (n + five_to_four * 4) / (count + five_to_four)
                        session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                                  message='До 5-ки пятерок: ' + str(five_to_five) + '\n' +
                                                  'До 4-ки пятерок: ' + str(five_to_four) + '\n' +
                                                  'До 4-ки четверок: ' + str(four_to_four) + '\n' + '\n' +
                                                  'Текущий средний бал: ' + str(av))
                        break
                    else:
                        session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                                  message='Некорректный ввод! Пожалуйста, попробуйте заново.')
                        break

        elif event.text == 'Википедия':
            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard, message='Введите запрос.')
            for event_w in longpoll.listen():
                if event_w.type == VkEventType.MESSAGE_NEW and event_w.to_me and event_w.text:
                    if event_w.from_user:
                        try:
                            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                                      message='Вот что я нашёл: \n' + str(wikipedia.summary(event_w.text)) +
                                                      '\n' + str(wikipedia.page(event_w.text).url))
                        except wikipedia.exceptions.PageError and wikipedia.exceptions.DisambiguationError:
                            session_api.messages.send(user_id=event.user_id, random_id='', keyboard=keyboard,
                                                      message='К сожалению, я не могу найти статью на данную тему.')
                        break
        else:
            text = random.choice(idk_phrases)
            session_api.messages.send(user_id=event.user_id, random_id='',
                                      message=text)










































