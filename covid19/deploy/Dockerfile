FROM python:3.7

USER root

RUN adduser --uid 1000 --disabled-password --gecos '' dash

COPY --chown=dash:dash ./app /app

WORKDIR /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8050

USER dash

CMD ["bash", "/app/start.sh"]
