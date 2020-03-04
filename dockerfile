FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

# Override the base image's uwsgi.ini file with our own
ENV UWSGI_INI uwsgi.ini
