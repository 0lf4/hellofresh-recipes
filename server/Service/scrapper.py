import json
from time import sleep
import random
import os
import logging

from datetime import datetime
from bs4 import BeautifulSoup
import urllib3
import re
from server.Service.database import Database
from server.Entity.recipe import Recipe
from server.appConfig import properties


def get_http_pool():
    user_agent = {'user-agent': properties.get_app_property("user_agent")}
    return urllib3.PoolManager(2, headers=user_agent)


def fetch_url_content(http, url):
    req = http.request('GET', url)
    return BeautifulSoup(req.data.decode('utf-8'), 'html.parser')


def parent_contains_plans_href(html_element):
    target_href = "/plans"
    pattern = re.compile(target_href)

    parent = html_element.find_parent(href=pattern)
    if parent:
        return True

    return False


def extract_tags(soup, recipe_global_info):
    tags = [tag.get_text(separator="").replace("•", "") for tag in
            soup.find_all(attrs={"data-test-id": "recipe-description-tag"})]
    if not tags:
        tags = [recipe_global_info.span.string]
        if parent_contains_plans_href(recipe_global_info.span):
            tags = []
    return tags


def extact_allergen(recipe_global_info):
    try:
        allergen_list = [allergen_list.find_all('span') for allergen_list in
                         recipe_global_info.find_all(attrs={"data-test-id": "recipe-description-allergen"})]
        allergen_list = [allergen[1].string if len(allergen) > 1 else allergen[0].string for allergen in allergen_list]
    except:
        allergen_list = []
    return allergen_list


def extract_ingredients(soup):
    recipe_ingredients_info = soup.find_all(attrs={"data-test-id": "ingredients-list"})[0]

    ingredients_shipped = [ingredients_shipped.find_all('p') for ingredients_shipped in
                           recipe_ingredients_info.find_all(attrs={"data-test-id": "ingredient-item-shipped"})]
    ingredients_not_shipped = [ingredients_not_shipped.find_all('p') for ingredients_not_shipped in
                               recipe_ingredients_info.find_all(attrs={"data-test-id": "ingredient-item-not-shipped"})]

    ingredients_list = [[ingredients[0].string, ingredients[1].string] for ingredients in ingredients_shipped] + [
        [ingredients[0].string, ingredients[1].string] for ingredients in ingredients_not_shipped]
    return ingredients_list


def extract_nutrition(soup):
    nutritions = [nutrition.get_text(separator="") for nutrition in
                  soup.find_all(attrs={"data-test-id": "nutritions"})[0].find_all(
                      attrs={"data-test-id": "items-per-serving"})[0].find_all('span')]
    nutrition = [nutritions[i:i + 2] for i in range(0, len(nutritions), 2)]
    return nutrition


def extract_utensils(soup):
    try:
        utensils = [utensil.get_text(separator="").replace("•", "") for utensil in
                    soup.find_all(attrs={"data-test-id": "utensils"})[0].find_all(
                        attrs={"data-test-id": "utensils-list-item"})]
    except:
        utensils = []
    return utensils


def extract_instructions(soup):
    instructions = [instruction.find_all('span') for instruction in
                    soup.find_all(attrs={"data-test-id": "instruction-step"})]
    instructions = [[instruction[0].string, instruction[1].get_text(separator=" ")] for instruction in instructions]
    return instructions


def extract_pdf(soup, http, title):
    try:
        recipe_pdf = soup.find_all(attrs={"data-test-id": "instructions"})[0].find('a')['href']
        pdf_local = properties.get_app_property("pdf_save_path").replace("seed-me", title.lower().replace(" ", "_"))

        download_pdf(http, recipe_pdf, pdf_local)

    except:
        recipe_pdf = ''
        pdf_local = ''
    return recipe_pdf, pdf_local


def download_pdf(http, recipe_pdf, pdf_local):
    pdf_file = http.request('GET', recipe_pdf)
    with open(pdf_local, 'wb') as f:
        f.write(pdf_file.data)

    while not os.path.exists(pdf_local):
        logging.info(f"Waiting for the file to be downloaded...")
        sleep(1)


def process_recipe_url(http, url):
    soup = fetch_url_content(http, url)
    data = soup.find_all(attrs={"data-test-id": "recipe-description"})

    if len(data) == 0:
        soup = fetch_url_content(http, url)

    recipe_global_info = data[0]

    title = recipe_global_info.h1.string
    tags = extract_tags(soup, recipe_global_info)
    allergen_list = extact_allergen(recipe_global_info)

    difficulty_level = \
    recipe_global_info.find_all(attrs={"data-translation-id": re.compile("recipe-detail.level-number")})[0].string
    prep_time = (recipe_global_info.find_all(
        attrs={"data-translation-id": "recipe-detail.preparation-time"})[0]
                 .string.next_element.string)

    ingredients_list = extract_ingredients(soup)
    nutrition = extract_nutrition(soup)
    utensils = extract_utensils(soup)
    instructions = extract_instructions(soup)

    recipe_pdf, pdf_local = extract_pdf(soup, http, title)

    try:
        doc = json.dumps(Recipe(
            url=url, name=title, difficulty=difficulty_level, time=prep_time, created_at=str(datetime.now()),
            pdf_origin=recipe_pdf, pdf_local=pdf_local, tags=tags, allergen=allergen_list, ingredients=ingredients_list,
            nutrition=nutrition, utensils=utensils, instructions=instructions).to_json())

        database = Database()
        database.insert(index_name='recipe', doc=doc)
    except:
        logging.error(f"Error while inserting the recipe: {url}", exc_info=True)

    sleep(random.uniform(9.9, 20.1))


def start_scrapping(sitemap):
    http = get_http_pool()

    soup_sitemap = fetch_url_content(http, sitemap)
    url_list = [adr_list.string for adr_list in soup_sitemap.find_all('loc')]

    for url in url_list:
        logging.info(f'Current address: {url}')
        process_recipe_url(http, url)

    return True
