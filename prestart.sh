#!/bin/bash

# Check to see if the container has the Wiktionary data.
# If it doesn't, download it in /data.
DATA_FILE=data/enwiktionary-latest-pages-articles.xml.bz2
if test -f "$DATA_FILE"; then
  echo "File $DATA_FILE already exists, not downloading the Wiktionary data"
else
  curl https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2 -o data/enwiktionary-latest-pages-articles.xml.bz2
fi

# Let's check to see if Elasticsearch is up and running and if the index exists.
set -e
host="http://elasticsearch:9200"

until $(curl --output /dev/null --silent --head --fail "$host"); do
  printf '. waiting on ES!'
  sleep 1
done

# First wait for ES to start.
response=$(curl $host)

until [ "$response" = "200" ]; do
  response=$(curl --write-out %{http_code} --silent --output /dev/null "$host")
  >&2 echo "Elastic Search is unavailable - sleeping"
  sleep 1
done


# Next wait for ES status to turn to green.
health="$(curl -fsSL "$host/_cat/health?h=status")"
# trim whitespace (otherwise we'll have "green ")
health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')"

until [ "$health" = 'green' ]; do
  health="$(curl -fsSL "$host/_cat/health?h=status")"
  health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')"
  >&2 echo "Elastic Search is unavailable - sleeping"
  sleep 1
done

>&2 echo "Elastic Search is up"

# Now check if the index exists. If it doesn't, run the script to
# create the index and insert Wiktionary data.
expected_index="$host/dictionary"
response=$(curl --write-out %{http_code} --silent --output /dev/null "$expected_index")
echo "ES INDEX VALUE - $response"
if [ "$response" = "404" ]; then
  echo "Running data ingest"
  ./bin/wik_extract "$DATA_FILE" &
fi
