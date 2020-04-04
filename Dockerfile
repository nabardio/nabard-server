FROM python:3
LABEL MAINTAINER="mehdy.khoshnoody@gmail.com"

ENV PYTHONBUFFERED 1

RUN pip install gunicorn gevent pipenv

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 8000

RUN pipenv install --system

ENTRYPOINT ["./entrypoint.sh"]
