import requests
from bs4 import BeautifulSoup


def get_ingredient(url: str):
    """"
    Sometimes in `quantity` comes across ½ so I changed to 0,5
    On site quantity and unit in one string, so I split them by " ", but if `quantity` undefined then
    `quantity` = "по вкусу", so I replaced -> "по-вкусу None", unit = None

    :param url: Get url of each dish from MainParser.py
    :return: ingredients: list | quantity_portion: int
    """

    response = requests.get(url)
    beautiful_soup = BeautifulSoup(response.text, 'lxml')  # parsing html code

    ingredients = []  # list of all ingredients that dish have
    quantity_portion = int(beautiful_soup.find("div", class_="emotion-1047m5l").text)
    ing_info = beautiful_soup.find_all('div', class_='emotion-7yevpr')

    for ingredient in ing_info:
        name = ingredient.find("span", itemprop="recipeIngredient").text.replace("'", "’")
        quantity = ingredient.find("span", class_="emotion-15im4d2").text.replace("½", "0,5")  # "½ кг" -> "0.5 кг"
        # 'Соль|по|вкусу' -> 'Соль|0|по-вкусу'
        quantity = quantity.replace("на кончике ножа", "0 на кончике ножа").replace(
            "¼", "0,25").replace("щепотка", "0 щепотка").replace("по вкусу", "0 по-вкусу").split(' ')

        ingredients.append([name, quantity[0], " ".join(quantity[1:])])  # ['Томатная паста', '2', 'столовые ложки']

    return ingredients, quantity_portion
