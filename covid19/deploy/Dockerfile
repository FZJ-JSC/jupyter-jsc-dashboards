FROM python:3.7

USER root

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG de_DE.UTF-8
ENV LC_ALL de_DE.UTF-8

RUN adduser --uid 1007 --disabled-password --gecos '' dash

COPY --chown=dash:dash ./requirements.txt /requirements.txt

RUN pip install --trusted-host pypi.python.org -r /requirements.txt

COPY --chown=dash:dash ./app /app

RUN mkdir -p /app/cache && chown dash:dash /app/cache

WORKDIR /app

EXPOSE 8050

USER dash

CMD ["bash", "/app/start.sh"]
