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


def get_film_by_id(film_id):
    movie = Movie(id=int(film_id))
    movie.get_content("main_page")
    return movie


async def load_posters(film_obj):
    # СИЛЬНО ЗАТОРМАЖИВАЕТ РАБОТУ!!!!
    # Пока не знаю как решить. Буду пробовать с asyncio

    film_obj.get_content("posters")
    return film_obj.posters[:1]

def get_full_data(id_of_film):
    movie_obj = get_film_by_id(id_of_film)
    movie_posters = load_posters(movie_obj)

    message_text = format_text(movie_obj.title, movie_obj)


def format_text(film_name, movie_obj, format="short"):
    message_text = "*Название:* _{0}_ \n".format(film_name)
    if movie_obj.rating:
        message_text += "*Рейтинг:* " + "⭐" * int(movie_obj.rating) + "\n\n"

    if format == "short" and len(movie_obj.plot) > 100:
        movie_obj.plot = movie_obj.plot[:100] + " ..."

    message_text += "*Описание:* {0}".format(movie_obj.plot)
    return message_text


def create_keyboard_films(film_name):
    film_names = get_movies_by_name(film_name)

    if film_names:  # В случае, если вообще существуют такие фильмы.
        movie_dict_data = get_movies_desc(*film_names)

        ready_elems = []
        id_in = 0

        for film in movie_dict_data:
            if movie_dict_data[film]:
                movie_obj = movie_dict_data[film]

                # Создание сообщения для краткого ответа
                message_text = format_text(film_name=film, movie_obj=movie_obj)
                message_content = telebot.types.InputTextMessageContent(message_text=message_text,
                                                                        parse_mode="Markdown")

                # Создание клавиатуры
                kb = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton(text="Открыть обсуждение",
                                                         callback_data=str(movie_obj.id))
                kb.add(btn)

                # Новый элемент
                new_elem = telebot.types.InlineQueryResultArticle(
                    id=str(id_in),
                    title=film,
                    input_message_content=message_content,
                    reply_markup=kb
                )

                id_in += 1
                ready_elems.append(new_elem)
            else:
                continue

        return ready_elems
    else:
        return []


def get_movies_by_name(film_name):
    # Получаем список фильмов по названию.
    list_of_movies = Movie.objects.search(film_name)

    if list_of_movies:

        if len(list_of_movies) > 4:
            return list_of_movies[:4]

        else:
            return list_of_movies

    else:
        return []


def get_movies_desc(*films):
    # print(films)
    dict_to_return = {}

    for film in films:
        movie = Movie(id=film.id)
        movie.get_content("main_page")

        dict_to_return.update(
            {
                movie.title: movie
            }
        )

    return dict_to_return


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    # print(query)
    result = create_keyboard_films(query.query)

    bot.answer_inline_query(query.id, result)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    print(call)
    movie_obj = get_film_by_id(call.data)
    poster = yield from load_posters(movie_obj)
    print(poster)
    bot.edit_message_text(inline_message_id=call.inline_message_id, text="Hello, guys!")


bot.polling(none_stop=True)