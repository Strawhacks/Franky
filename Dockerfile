FROM python:3.8

RUN mkdir -p /app/root

COPY bot.py /app/root
COPY Pipfile /app/root
COPY Pipfile.lock /app/root

WORKDIR /app/root

RUN python -m pip install pipenv
RUN python -m pipenv install

ENTRYPOINT python -m pipenv run python bot.py
