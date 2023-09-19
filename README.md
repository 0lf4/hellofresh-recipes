# hellofresh-recipes
Retrieve recipes from the HelloFresh website and store them in either Elasticsearch or MongoDB

## How to start the application
### Prerequisites
* Python 3.11
* Poetry
* Docker
* Docker Compose
* Elasticsearch (optional)
* MongoDB (optional)
* Kibana (optional)

### Installation
1. Clone the repository
2. Install the dependencies with `poetry install`
3. Create a `properties.toml` file in the root of the project and add the following environment variables:
    * `sitemap_url`
    * `user_agent`
    * `pdf_save_path`
    * `url`
    * `username`
    * `password`
    * `type`
   
Take a look at the `properties.example.toml` file for an example.

### Run the application
1. Run `docker-compose up -d` to start the database
You may need to change the `docker-compose.yml` file to match your database settings.
2. Run `poetry run python scrapper.py` to start the application
