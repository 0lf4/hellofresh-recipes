import json
from time import sleep
import random
import os
import logging

from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import re
from Service.database import Database
from Entity.recipe import Recipe
from appConfig import properties


def parent_contains_plans_href(html_element):
    target_href = "/plans"
    pattern = re.compile(target_href)

    parent = html_element.find_parent(href=pattern)
    if parent:
        return True

    return False


database = Database()
sitemap = properties.get_app_property("sitemap_url")

user_agent = {'user-agent': properties.get_app_property("user_agent")}
http = urllib3.PoolManager(2, headers=user_agent)

req = http.request('GET', sitemap)

url_list = [adr_list.string for adr_list in BeautifulSoup(req.data.decode('utf-8'), 'html.parser').find_all('loc')]

for url in url_list:

    logging.info(f'Current address: {url}')

    req = http.request('GET', url)
    soup = BeautifulSoup(req.data.decode('utf-8'), 'html.parser')

    if len(soup.find_all(attrs={"data-test-id": "recipe-description"})) == 0:
        req = http.request('GET', url)
        soup = BeautifulSoup(req.data.decode('utf-8'), 'html.parser')

    recipe_global_info = soup.find_all(attrs={"data-test-id": "recipe-description"})[0]
    title = recipe_global_info.h1.string

    tags = [tag.get_text(separator="").replace("•", "") for tag in
           soup.find_all(attrs={"data-test-id": "recipe-description-tag"})]

    if len(tags) == 0:
        tags = [recipe_global_info.span.string]
        print(tags)
        if parent_contains_plans_href(recipe_global_info.span):
            tags = []

    try:
        allergen = recipe_global_info.find_all(attrs={"data-translation-id": "recipe-detail.allergens"})[0].string
        allergen_list = [allergen_list.find_all('span') for allergen_list in recipe_global_info.find_all(attrs={"data-test-id": "recipe-description-allergen"})]
        allergen_list = [allergen[1].string if len(allergen) > 1 else allergen[0].string for allergen in allergen_list]
    except:
        allergen = ''
        allergen_list = []

    difficulty = recipe_global_info.find_all(attrs={"data-translation-id": "recipe-detail.difficulty"})[0].string

    difficulty_level = recipe_global_info.find_all(attrs={"data-translation-id": re.compile("recipe-detail.level-number")})[0].string

    prep_time = recipe_global_info.find_all(attrs={"data-translation-id": "recipe-detail.preparation-time"})[0].string
    prep_time = prep_time.next_element.string

    recipe_ingredients_info = soup.find_all(attrs={"data-test-id": "ingredients-list"})[0]

    ingredients_shipped = [ingredients_shipped.find_all('p') for ingredients_shipped in recipe_ingredients_info.find_all(attrs={"data-test-id": "ingredient-item-shipped"})]
    ingredients_not_shipped = [ingredients_not_shipped.find_all('p') for ingredients_not_shipped in recipe_ingredients_info.find_all(attrs={"data-test-id": "ingredient-item-not-shipped"})]

    ingredients_list = [[ingredients[0].string, ingredients[1].string] for ingredients in ingredients_shipped] + [[ingredients[0].string, ingredients[1].string] for ingredients in ingredients_not_shipped]

    nutritions = [nutrition.get_text(separator="") for nutrition in soup.find_all(attrs={"data-test-id": "nutritions"})[0].find_all(attrs={"data-test-id": "items-per-serving"})[0].find_all('span')]
    nutrition = [nutritions[i:i+2] for i in range(0, len(nutritions), 2)]

    try:
        utensils = [utensil.get_text(separator="").replace("•", "") for utensil in soup.find_all(attrs={"data-test-id": "utensils"})[0].find_all(attrs={"data-test-id": "utensils-list-item"})]
    except:
        utensils = []

    try:
        recipe_pdf = soup.find_all(attrs={"data-test-id": "instructions"})[0].find('a')['href']
        pdf_local = properties.get_app_property("pdf_save_path").replace("seed-me", title.lower().replace(" ", "_"))

        pdf_file = http.request('GET', recipe_pdf)
        with open(pdf_local, 'wb') as f:
            f.write(pdf_file.data)

        while not os.path.exists(pdf_local):
            logging.info(f"Waiting for the file to be downloaded...")
            sleep(1)

    except:
        recipe_pdf = ''
        pdf_local = ''

    instructions = [instruction.find_all('span') for instruction in soup.find_all(attrs={"data-test-id": "instruction-step"})]
    instructions = [[instruction[0].string, instruction[1].get_text(separator=" ")] for instruction in instructions]

    try:
        doc = json.dumps(
            Recipe(
                url=url, name=title, difficulty=difficulty_level, time=prep_time, created_at=str(datetime.now()),
                pdf_origin=recipe_pdf, pdf_local=pdf_local, tags=tags, allergen=allergen_list, ingredients=ingredients_list,
                nutrition=nutrition, utensils=utensils, instructions=instructions
            ).to_json())

        database.insert(index_name='recipe', doc=doc)
    except:
        logging.error(f"Error while inserting the recipe: {url}", exc_info=True)

    sleep(random.uniform(9.9, 20.1))

