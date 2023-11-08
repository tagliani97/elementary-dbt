# Use uma imagem base com Python 3.8 (ou qualquer versão compatível)
FROM python:3.8

RUN apt-get update && \
    apt-get install -y \
    git \
    && apt-get clean

RUN pip install dbt-postgres==1.6.6 dbt-core==1.6.6 dbt-athena-community==1.6.3 git+https://github.com/artem-garmash/elementary@athena-support-v3-ci

RUN git clone https://github.com/dbt-labs/jaffle_shop

ENV DBT_PROFILES_DIR=/jaffle_shop
