FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 9200

RUN ["chmod", "+x", "/app/docker-entrypoint.sh"]

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
