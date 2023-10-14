# hellofresh-recipes
Retrieve recipes from the HelloFresh website and store them in either Elasticsearch or MongoDB

## How to start the application in dev environment
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
2. Install the dependencies for the backend app in `/server` folder with :
   > poetry install
3. Install the dependencies for the frontend app in `/client/front` folder with :
   > npm install
4. Create a `properties.toml` file in `/server` folder and add the following environment variables:
    * `SITEMAP_URL`
    * `USER_AGENT`
    * `PDF_SAVE_PATH`
    * `URL`
    * `USERNAME`
    * `PASSWORD`
    * `TYPE`
5. Create a `.env.local` file in `/client/front` folder and add the following environment variable:
   * `VITE_API_URL`
   
Take a look at the `properties.example.toml` file for an example.\
:warning: For the `sitemap_url` you need to let **seed-me** as extension.


### Run the application
1. Start the database of your choice (ATM only ElasticSearch is supported).\
If you want a quick setup for ElasticSearch, take a look in /bin/ElasticSearchKibana.\
You just need to create a `.env` file with correct fields.\
As below, take a look at `env-exemple`.

2. If you're not using the quick setup for ElasticSearch, go to step 3.\
   You may need to change the `docker-compose.yml` file to match your database settings.\
   Run the compose command :
     > docker-compose up -d

   If you are facing an issue with max virtual memory allocated:
   * On Linux just run this command (It's a none permanent change):
     >    sudo sysctl -w vm.max_map_count=262144

   * On Windows you need to run the same command but in your **WSL 2** environment.

3. To start the backend application,\
   Manually:
   * First, go into `/server` and run:
     > poetry shell
   
   * Then, go back to the root project `hellofresh-recipes` and run 
     > python -m uvicorn server.main:app --reload
   
   With docker:\
   Go in `/bin` folder and run:
   > ./build_and_start_backend.sh
   
4. To start the web application,\
   Manually:
   Go in `/client/front` folder and run
   >  npm run dev
   
   With docker:\
   Go in `/bin` folder and run:
   > ./build_and_start_front.sh

### Endpoints list
   * Backend endpoints, run the app and add **docs** at the end of the url. e.g. `http:localhost:8000/docs`\
   * Frontend endpoints, *Not implemented yet*