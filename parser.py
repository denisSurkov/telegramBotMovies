import urllib.request
from bs4 import BeautifulSoup

START_URL = "https://www.kinopoisk.ru/top/lists/"
FILT_ATTR = "filtr/all/sort/order/page/%d/"
TXT_FILE = "parsed_films_all_%d.txt"


def get_table_category(html):
    soup = BeautifulSoup(html)
    main_list = soup.find("div", class_="list_main")
    elements_in_main = main_list.find_all("li")
    id_of_lists = []
    for li in elements_in_main:
        link_div = li.find("div", class_="link")
        if not link_div:
            continue
        current_href = link_div.a["href"]
        current_id_list = current_href.split("/")[-2]
        id_of_lists.append(current_id_list)
    return id_of_lists


def get_categories(html):
    soup = BeautifulSoup(html)
    page_top = soup.find("ul", class_="list_top")
    li_elem = page_top.find_all("li")
    categories = []
    for category in li_elem:
        try:
            current_href = category.a["href"]
        except TypeError:
            current_href = "/top/lists/kinopoisk/"
        current_name = current_href.split("/")[-2]
        categories.append(current_name)
    return categories


def count_pages(html):
    soup = BeautifulSoup(html)
    page_div = soup.find("div", class_="navigator")
    try:
        last_page_href = page_div.find_all("a")[-1]["href"]
    except IndexError:
        last_page_num = 2
    else:
        last_page_num = int(last_page_href.split("/")[-2])
    return last_page_num


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, "html")
    table = soup.find("table", id="itemList")
    rows = table.find_all("tr")
    film_names = []
    for row in rows:
        cols = row.find_all("td")
        try:
            name = str(cols[1].div.a.text)
        except IndexError:
            continue
        film_names.append(name)
    return film_names


def main():
    html = get_html(START_URL)
    categories = get_categories(html)

    for category in categories:
        category_url = START_URL + category + "/"
        cur_html = get_html(category_url)
        cur_table = get_table_category(cur_html)

        print("-> Начали парсить категорию {0}".format(category))

        for item_id in cur_table:
            cur_url = START_URL + str(item_id) + "/"
            cur_in_row_html = get_html(cur_url)
            last_page_num = count_pages(cur_in_row_html)

            films_name = []
            print("-> Парсим {0}".format(item_id))
            for num_page in range(1, last_page_num + 1):
                html = get_html(cur_url + FILT_ATTR % num_page)
                films = parse(html)
                films_name.extend(films)

                print("\tСпарсили %d" % int((num_page / last_page_num * 100)))

            create_file(*films_name, num=int(item_id))



def create_file(*film_names, num):
    # print(film_names)
    with open(TXT_FILE % num, "w", encoding="utf-8") as txt:
        for film in film_names:
            txt.write(film + "\n")


if __name__ == "__main__":
    main()