import os
import logging
from .Service import scrapper

from fastapi import FastAPI, Query, Path, HTTPException
from typing import List
from starlette.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from starlette.responses import FileResponse
from .appConfig import properties

app = FastAPI()

origins = [
    # "http://localhost:8000",
    # "http://localhost:5173",
    # "http://locahost:3000"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GLOBAL VARIABLES
SITEMAP_SEED = properties.get_app_property("sitemap_url")

ES_URL = properties.get_database_property("url")
ES_USERNAME = properties.get_database_property("username")
ES_PASSWORD = properties.get_database_property("password")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdf_folder")
# END GLOBAL VARIABLES


@app.get("/health")
async def health():
    """
    Health check
    :return: a json with status ok
    """
    return {"status": "ok"}


@app.get("/")
async def root():
    """
    Return a list with the 6 first recipes
    :return: the list of 6 recipes
    """

    es = Elasticsearch(
        hosts=ES_URL,
        basic_auth=(ES_USERNAME,
                    ES_PASSWORD),
        verify_certs=False)

    query = {
        "query": {
            "match_all": {}
        }
    }

    try:
        response = es.search(index='recipe', body=query, size=10000)
        return {'data': response["hits"]["hits"][0:6]}
    except Exception as e:
        print(f"Error: {e}")
        return None


@app.get("/weekly-recipe/")
async def weekly_recipe(filter: List[str] = Query(None)):
    """
    Return a list of 10 random recipes
    :param filter: list of filters
    :return: a list of 10 recipes
    """

    exclude_condition = []
    if filter is not None:
        for item in filter:
            for field in ["name", "tags", "allergen"]:
                exclude_condition.append({"match": {field: item}})

    es = Elasticsearch(
        hosts=ES_URL,
        basic_auth=(ES_USERNAME,
                    ES_PASSWORD),
        verify_certs=False)

    query = {
        "size": 10,
        "query": {
              "function_score": {
                "query": {
                    "bool": {
                        "must_not": exclude_condition
                    }
                },
                "functions": [
                    {
                        "random_score": {}
                    }
                ],
                "boost_mode": "replace"
              }
        }
    }

    response = es.search(index='recipe', body=query, request_cache=False)

    return {'data': response["hits"]["hits"]}


@app.get("/change-one/")
async def change_one(ids: str = Query(None), filter: List[str] = Query(None)):
    """
    Return a random recipe
    :param ids: list of ids to exclude
    :param filter: list of filters
    :return: a random recipe
    """

    if ids is None:
        raise HTTPException(status_code=404, detail="ids not found")
    exclude_ids = ids.split('&&')
    logging.info(exclude_ids)

    exclude_condition = []
    if filter is not None:
        for item in filter:
            for field in ["name", "tags", "allergen"]:
                exclude_condition.append({"match": {field: item}})

    if exclude_ids:
        exclude_condition.append({"terms": {"_id": exclude_ids}})

    must_not_conditions = exclude_condition + [
        {
            "ids": {
                "values": exclude_ids  # Assuming exclude_ids is a list
            }
        }
    ]

    es = Elasticsearch(
        hosts=ES_URL,
        basic_auth=(ES_USERNAME,
                    ES_PASSWORD),
        verify_certs=False)

    query = {
        "size": 1,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must_not": must_not_conditions
                    }
                },
                "functions": [
                    {
                        "random_score": {}
                    }
                ],
                "boost_mode": "replace"
            }
        }
    }

    response = es.search(index='recipe', body=query, request_cache=False)

    return {'data': response["hits"]["hits"]}


@app.get("/pdf/")
async def pdf(pdf_path: str = Query(None)):
    """
    Return the pdf file
    :param pdf_path: path of the pdf
    :return: the pdf file
    """

    logging.info(pdf_path)

    pdf_path = os.path.basename(pdf_path)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")


@app.get("/web_service/")
async def web_service(lang: str = Query(None)):
    """Start the scrapping of the website
    :param lang: language of the website
    :return: a boolean informing if completed"""

    list_lang = ['EN', 'US', 'FR', 'DE', 'ES', 'NL', 'BE', 'LU', 'CH', 'IT']

    if (lang is None) or (lang == '') or (lang not in list_lang):
        raise HTTPException(status_code=404, detail="Language not found")

    sitemap = SITEMAP_SEED.replace("seed-me", lang.lower())
    logging.info(f'Start Scrapping')
    completed = scrapper.start_scrapping(sitemap)

    return {'completed': completed}



