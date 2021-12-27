FROM python:3.8.6-slim

ENV PYTHONUNBUFFERED 1

COPY pdf_generator/requirements.txt /requirements.txt
# Install python and postgres dependencies under a virtual package
RUN pip install --upgrade pip -r /requirements.txt
RUN apt update
RUN apt install --yes wkhtmltopdf
# Delete virtual packages as we installed our dependencies

RUN mkdir /app
WORKDIR /app
COPY ./pdf_generator /app
RUN python3 manage.py collectstatic --noinput