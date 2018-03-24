import sqlite3
import glob
#from kinopoisk.movie import Movie
import http.client
import urllib.parse
import json


connection = sqlite3.connect("sqlite3.db")
cursor = connection.cursor()
conn_http = http.client.HTTPSConnection("api.themoviedb.org")


def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS films VALUES (
    title STRING,
    plot TEXT,
    runtime INT,
    rating FLOAT,
    year INT""")
    connection.commit()


def get_info_film(name):
    exportData = {'page': '1',
                  'query': name,
                  'language': 'ru',
                  'api_key': API_KEY}
    payload = "{}"
    data_to_send = urllib.parse.urlencode(exportData)
    conn_http.request("GET", "/3/search/movie?" + data_to_send, payload)
    res = conn_http.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    kek = json.loads(data)


def add_to_table(movie):
    cursor.execute("")

def read_files(file):
    film_names = []
    with open(file, "r", encoding="utf-8") as txt:
        whole_films = txt.read().split("\n")
        for film in whole_films:
            film_names.append(film)
    return film_names


def get_files():
    all_txt_files = glob.glob("..\*.txt")
    return all_txt_files


def main():
    #f = get_files()[0]
    #print(read_files(f))
    pass



if __name__ == "__main__":
    main()