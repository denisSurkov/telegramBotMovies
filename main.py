import asyncio
import os
import telebot
import logging
from kinopoisk.movie import Movie
from Main.consts_answers import Constants

bot = telebot.TeleBot("")

@bot.message_handler(commands=["start", "help"])
def greeting(message):
    bot.send_message(message.chat.id, Constants.greeting_msg)

'''
@bot.message_handler()
def get_movie_by_msg(message):
    film = message.text
    list_of_movie = Movie.objects.search(film)
    first_movie_id = list_of_movie[0].id
    first_movie_obj = Movie(id=first_movie_id)
    first_movie_obj.get_content("main_page")
    first_movie_obj.get_content("posters")


    bot.send_message(message.chat.id, first_movie_obj.title + "\n" + first_movie_obj.plot)
    bot.send_photo(message.chat.id, first_movie_obj.posters[0])
'''
def create_keyboard_films(name_film):
    film_names = get_movie_by_name(name_film)
    films_and_posters = get_posters_movies(film_names)

    print(films_and_posters)

    ready_elems = []
    id_in = 0

    for film in films_and_posters:
        new_elem = telebot.types.InlineQueryResultPhoto(
            id=str(id_in),
            photo_url=films_and_posters[film],
            title=film
        )
        id_in += 1
        ready_elems.append(ready_elems)

    ready_elems.reverse()

    print(ready_elems)

    return ready_elems

def get_movie_by_name(name):
    list_of_movies = Movie.objects.search(name)


    if len(list_of_movies) > 10 or len(list_of_movies) == 0:
        return list_of_movies[:5]
        pass
    else:
        return list_of_movies

def get_posters_movies(*films):
    posters = {

    }

    print(films)

    for film in films:
        movie = Movie(id=film[0].id)

        movie.get_content("main_page")
        movie.get_content("posters")
        posters.update({
                movie.title: movie.posters[0]
            })

    return posters


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = telebot.types.InlineKeyboardMarkup()
    print(query)
    # Добавляем колбэк-кнопку с содержимым "test"
    kb.add(telebot.types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = create_keyboard_films(query.query)

    '''
    smth = get_movie_by_name(query.query)
    single_msg = telebot.types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=telebot.types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    '''

    bot.answer_inline_query(query.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    print(call)
    bot.edit_message_text(inline_message_id=call.inline_message_id, text="Hello, guys!")


    """
    if call.message:
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")
    """

bot.polling(none_stop=True)