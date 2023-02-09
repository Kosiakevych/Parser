import requests
from bs4 import BeautifulSoup
from search_equipment import check_equipment, translate


def cooking_time(text: str) -> int:
    """
    The point of this function is take "1 hour 30 min" -> 90
    For Django filter -> Find all dish that less or equal than 90 min
    :param text: `get_time` from `get_data` -> 1 hour 30 minute | 5 minute
    :return: "1 hour 30 min" -> 90
    """
    total = 0  # What we will return
    text = text.split(" ")  # "1 hour 30 min" -> ["1", "hour", "30", "min",]
    for word in text:
        if "час" in word:
            total += 60 * int(text[0])
        if "ми" in word:
            total += int(text[text.index(word) - 1])  # ["1", "hour", "30", "min",] min id = 3 -> 3 - 1 = "30"
    return total


def get_data(url: str):
    """
    Sometimes dish hasn't desrciprion, so I check and if dish hasn't then `desrciprion` return None.
    And sometimes instruction image, so I check: If dish has no image then `image` return None and
    if dish has no image then div for `number` change.
    Also, we used list(set(list with equipment)) to will not get the same equipment more than one, then
    We used `equipment_for_sql` to get list for SQL

    :param url: Get url of each dish from MainParser.py.
    :return: desrciprion: str | instruction_data: list | energy value(4): int | get_time: str | equipment: list
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')  # parsing html code
    equipment = []  # list for all equipment we found in text instruction

    # if dish has no desrciprion -> None
    desrciprion = soup.find("span", class_="emotion-1x1q7i2")
    desrciprion = desrciprion.text.replace("&nbsp;", " ").replace("'", "’") if desrciprion else None

    # Get info of Instruction |(text -> str), (number -> int,) (image -> str)|
    instruction_info = soup.find_all("div", itemprop="recipeInstructions")  # block of instruction
    instruction_data = []  # list because in cycle for var are local

    for i in instruction_info:
        text = i.find("span", class_="emotion-6kiu05").text.replace("\xa0", " ").replace("\xad", " ").replace("'", "’")
        # if dish has no image -> div of number change
        number = i.find("div", class_="emotion-19fjypw")
        number = i.find("span", class_="emotion-bzb65q").text if not number else number.find("span").text

        instruction_data.append([text, number])
        # check equipment in `text`
        check_equipment(text, equipment)  # append list in list because var local
    # list for SQL
    equipment = translate(list(set(equipment)))  # ["Pan", "Microwave", "Pan"] -> ["Pan", "Microwave"]

    # Get energy value per serving -> all int
    calories = soup.find("span", itemprop="calories").text
    protein = soup.find("span", itemprop="proteinContent").text
    fat = soup.find("span", itemprop="fatContent").text
    carbohydrate = soup.find("span", itemprop="carbohydrateContent").text

    # Get time of cook -> str
    get_time = soup.find("div", class_="emotion-my9yfq").text  # 30 минут
    get_time_min = cooking_time(get_time)
    return desrciprion, instruction_data, calories, protein, fat, carbohydrate, get_time, equipment, get_time_min
