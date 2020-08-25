FROM python:3.7

USER root

RUN adduser --uid 1000 --disabled-password --gecos '' dash

COPY --chown=dash:dash ./requirements.txt /requirements.txt

RUN pip install --trusted-host pypi.python.org -r /requirements.txt

COPY --chown=dash:dash ./app /app

RUN mkdir -p /app/cache && chown dash:dash /app/cache

WORKDIR /app

EXPOSE 8050

USER dash

CMD ["bash", "/app/start.sh"]
