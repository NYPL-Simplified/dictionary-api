import os

ELASTIC_SEARCH_URL = os.environ.get('ELASTIC_SEARCH_URL', 'http://localhost:9200')
TEST_ELASTIC_SEARCH_URL = os.environ.get('TEST_ELASTIC_SEARCH_URL', 'http://localhost:9200')
