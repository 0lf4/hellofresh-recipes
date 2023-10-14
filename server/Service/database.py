from elasticsearch import Elasticsearch
from ..appConfig import properties
import json
import logging


class Database:
    def __init__(self):
        self._type = properties.get_database_property("TYPE").lower()
        self._valid_es_types = ["elastic", "elastic search", "elastic_search", "elasticsearch", "es"]
        self._valid_mongo_types = ["mongo", "mongodb", "mongo_db", "mongo db"]
        self._config = self._load_config()
        self._check_and_create_index()

    def _load_config(self):
        if self._type.lower() in self._valid_es_types:
            return Elasticsearch(
                hosts=properties.get_database_property("URL"),
                basic_auth=(properties.get_database_property("USERNAME"),
                            properties.get_database_property("PASSWORD")),
                verify_certs=False)

        elif self._type in self._valid_mongo_types:
            logging.error("Not implemented yet for MongoDB.")
            return None

        else:
            logging.error("Unsupported database type.", exc_info=True)
            raise ValueError("Unsupported database type.")

    # TODO : Do it one time at start, not everytime the class is instantiate
    def _check_and_create_index(self):
        indices = ["recipe", "menu"]
        for indice in indices:
           if not self._load_config().indices.exists(index=indice):
                self._load_config().indices.create(index=indice)
                logging.info(f"Index {indice} created.")
           else:
               logging.info(f"Index {indice} exist.")

    def search(self, index_name, doc):

        logging.info("Searching for document in ElasticSearch")
        parsed_doc = json.loads(doc)

        search_query = {
            "query": {
                "match_phrase": {
                    "name": parsed_doc['name']
                }
            }
        }

        result = self._load_config().search(index=index_name, body=search_query)

        if result['hits']['total']['value'] != 0:
            logging.info('Document already found in ElasticSearch')
            return True
        return False

    def insert(self, index_name, doc):

        logging.info("Inserting document in ElasticSearch")

        if self._type.lower() in self._valid_es_types:

            match index_name:
                case "recipe":
                    if self.search(doc=doc, index_name=index_name) is False:
                        self._load_config().index(index=index_name, document=doc)
                        logging.info("Document inserted")
                case "menu":
                    self._load_config().index(index=index_name, document=doc)
                    logging.info("Document inserted")
                case _:
                    logging.error("Unsupported index name.", exc_info=True)

        elif self._type in self._valid_mongo_types:
            logging.error("Not implemented yet for MongoDB.")

        else:
            logging.error("Unsupported database type.", exc_info=True)
            raise ValueError("Unsupported database type.")
