FROM python:3.7-slim

COPY ./requirements.txt /requirements.txt

RUN	apt-get update \
    && apt-get install -y build-essential \
    && pip3 install -r /requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean

COPY ./models.py /models.py
COPY ./app.py /app.py
COPY ./datasource.csv /datasource.csv
COPY ./uwsgi.ini /uwsgi.ini

ENTRYPOINT ["uwsgi", "/uwsgi.ini"]
