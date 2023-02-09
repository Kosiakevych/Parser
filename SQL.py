import pymysql
from config import *


connection = pymysql.connect(
    host=host,
    port=8889,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor)


def fill_list_of_dishes(name, image, description, time, time_min, slug, energy_id, category_id, cuisine_id):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `base_list_of_dish` "
                       f"(name, image, description, time, time_min, url, energy_value_id, category_id, cuisine_id) "
                       f"VALUES ('{name}','{image}', '{description}', "
                       f"'{time}', {time_min}, '{slug}', {energy_id}, {category_id}, {cuisine_id});")
        connection.commit()


def fill_energy_value(calories, proteins, fats, carbohydrates):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `base_energy_value` (calories, proteins, fats, carbohydrates) "
                       f"VALUES ({calories}, {proteins}, {fats}, {carbohydrates});")
        connection.commit()


def fill_instruction(number, instructionText):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `base_instruction` (number, text) "
                       f"VALUES ({number}, '{instructionText}');")
        connection.commit()


def fill_ingredients(name, quan, unit, default_quant):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `base_ingredients` (name, quantity, unit, default_quant) "
                       f"VALUES ('{name}', '{quan}', '{unit}', {default_quant});")
        connection.commit()


def get_id(name, table):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT `id` FROM `{table}` WHERE name = '{name}'")
        return cursor.fetchall()[0]["id"]


def fill_M2M(id_dish, second_id, table, second_id_name):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `{table}` (`list_of_dish_id`, `{second_id_name}`) "
                       f"VALUES ({id_dish}, {second_id});")
        connection.commit()


def fill_cuisine(name):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `base_cuisine` (name) "
                       f"VALUES ('{name}');")
        connection.commit()


def fill_all_ingredients(ingredient_id, name: str, description, image, category):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO `All_Ingredients` (IngredientID, Name, Description, image, Category) "
                       f"VALUES ({ingredient_id}, '{name}', '{description}', '{image}', '{category}');")
        connection.commit()
