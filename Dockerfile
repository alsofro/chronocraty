FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /app
COPY ./chronocraty /app