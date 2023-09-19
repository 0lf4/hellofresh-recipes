import os
import logging
from server.Service import scrapper

from fastapi import FastAPI, Query, Path, HTTPException
from typing import List
from starlette.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from starlette.responses import FileResponse
from server.appConfig import properties

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

sitemap_seed = properties.get_app_property("sitemap_url")


@app.get("/")
async def root():
    es = Elasticsearch(
        hosts=properties.get_database_property("url"),
        basic_auth=(properties.get_database_property("username"),
                    properties.get_database_property("paswword")),
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

    exclude_condition = []
    if filter is not None:
        for item in filter:
            for field in ["name", "tags", "allergen"]:
                exclude_condition.append({"match": {field: item}})

    es = Elasticsearch(
        hosts=properties.get_database_property("url"),
        basic_auth=(properties.get_database_property("username"),
                    properties.get_database_property("paswword")),
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

    exclude_condition = [{"match": {field: item}} for item in filter for field in ["name", "tags", "allergen"]]

    mustNotConditions = exclude_condition + [
        {
            "ids": {
                "values": exclude_ids  # Assuming exclude_ids is a list
            }
        }
    ]

    es = Elasticsearch(
        hosts=properties.get_database_property("url"),
        basic_auth=(properties.get_database_property("username"),
                    properties.get_database_property("paswword")),
        verify_certs=False)

    query = {
        "size": 1,
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must_not": mustNotConditions
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

    # query = {
    #     "size": 1,
    #     "query": {
    #           "function_score": {
    #             "query": {
    #                 "bool": {
    #                     "must_not":  exclude_condition
    #                 }
    #             },
    #             "functions": [
    #                 {
    #                     "random_score": {}
    #                 }
    #             ],
    #             "boost_mode": "replace"
    #           }
    #     }
    # }

                #GET /_search
                # {
                #   "query": {
                #     "bool": {
                #       "must_not": {
                #         "exists": {
                #           "field": "_id"
                #         }
                #       }
                #     }
                #   }
                # }


    response = es.search(index='recipe', body=query, request_cache=False)

    return {'data': response["hits"]["hits"]}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdf_folder")  # Make sure to place your PDFs here


@app.get("/pdf/")
async def pdf(pdf_path: str = Query(None)):

    logging.info(pdf_path)

    pdf_path = os.path.basename(pdf_path)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")


@app.get("/web_service/")
async def web_service(lang: str = Query(None)):

    list_lang = ['EN', 'US', 'FR', 'DE', 'ES', 'NL', 'BE', 'LU', 'CH', 'IT']

    if (lang is None) or (lang == '') or (lang not in list_lang):
        raise HTTPException(status_code=404, detail="Language not found")

    sitemap = sitemap_seed.replace("seed-me", lang.lower())
    logging.info(f'Start Scrapping')
    completed = scrapper.start_scrapping(sitemap)

    return {'completed': completed}



