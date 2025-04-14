FROM python:3.12-slim

WORKDIR /code
COPY . /code

RUN apt-get update && apt-get install -y curl && apt-get install -y netcat && apt-get clean

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --no-root

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]