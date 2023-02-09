import requests
from bs4 import BeautifulSoup
import time

from SQL import fill_all_ingredients


def get_each_url():
    site_url = f'https://eda.ru/wiki/ingredienty'
    gen_response = requests.get(site_url)
    all_item_soup = BeautifulSoup(gen_response.text, 'lxml')  # parsing html code
    data = all_item_soup.find_all("div", class_="emotion-mvfezh")

    for categories in data:
        url_categories = "https://eda.ru/wiki/" + categories.find("a").get("href")
        name_category = categories.find("span", "emotion-21sd8a").text
        yield url_categories, name_category


ingredient_id = 1
for url in get_each_url():  # get url of category
    page = 1
    while True:  # for all page in categories
        time.sleep(3)  # pause code to not break site
        response = requests.get(url[0] + f"?page={page}")
        page += 1  # ?page=1 -> ?page=2
        beautiful_soup = BeautifulSoup(response.text, 'lxml')  # parsing html code
        soup = beautiful_soup.find_all("div", class_="emotion-17kxgoe")  # for all ingredient we have in one page
        if not soup:  # if there is no more ingredient in page -> skip to the next page
            break
        for ing in soup:
            name = ing.find("h2", class_="emotion-ogw7y8").text
            try_description = ing.find("span", class_="emotion-9cuqpw")  # if ingredient has no description -> None
            description = try_description.text if try_description else None
            image = "https://eda.ru/" + ing.find("a").get("href")
            fill_all_ingredients(ingredient_id, name.replace("'", "’"), description, image, url[1])  # url[1] = category
            ingredient_id += 1


