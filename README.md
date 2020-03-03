# Library Simplified Dictionary API

## Local Development
This is a small API that depends on Elasticsearch 6. Once that is installed and running, the index needs to be built and populated with data.

First, download the base [Wiktionary data](https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2) that will be imported. This can go anywhere but `/data/enwiktionary-latest-pages-articles.xml.bz2` is suggested.

That data now needs to be ingested through a script found in `/bin`. Run `./bin/wik_extract data/enwiktionary-latest-pages-articles.xml.bz2` which will normalize and clean the Wiktionary data and then insert it into the Elasticsearch index. This is a long process but it can be stopped short if all of the data is not necessary to have.

Once the data is in Elasticsearch and that instance is running, for local development run `python app-dev.py`. The app will be available on `http://localhost:5000`.

# Production and Docker
For production-level startup, the app is expected to run behind nginx and uwsgi. The main file for that is in `/api/app.py`. This is the file that is used by Docker to start the app.

To build a Docker image, run `docker build -t dictionary-api:latest .`. This can be run using the `docker run` command. The current way to run this is using `docker-compose`. Running `docker-compose up` on the root directory will create all the images and containers that are needed, as well as start the app. The app will then be available on `http://localhost`.

Downloading the Wiktionary data, creating the Elasticsearch index, and ingesting the data are all done when the containers spin up.

The main api Docker image is using the [`uwsgi-nginx-flask-docker`](https://github.com/tiangolo/uwsgi-nginx-flask-docker) image as a base. This images spins up nginx and uwsgi for us but allows for overrides. Specifically, when the containers start we want to:
* check to see if the Wiktionary data that the API is using is as a base is available and downloads it if it's not
* run the Flask app once Elasticsearch is up
* checks to see if the needed Elasticsearch index is available
* if the index is not available, it is created and an ingest script runs in the background to populate it
