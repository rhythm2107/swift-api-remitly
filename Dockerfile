FROM python:3.12-slim

WORKDIR /code

# Only dependency for caching & faster building later
COPY pyproject.toml poetry.lock README.md /code/
COPY app /code/app

# Installing system deps, poetry, necessary tools etc.
RUN apt-get update \
 && apt-get install -y curl netcat-openbsd --no-install-recommends \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip poetry \
 && poetry install

COPY . /code

# Making helper scripts executable later
COPY scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]