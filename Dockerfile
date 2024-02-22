FROM apache/airflow:2.7.3

USER root

RUN apt-get update -y && \
    apt-get install -y \
    telnet \
    iputils-ping \
    python3 \
    python3-pip \
    git \
    vim \
    awscli \
    curl \
    ca-certificates \
    libffi-dev \
    libpq-dev \
    postgresql \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER airflow

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org \
    dbt-core psycopg2-binary dbt-postgres astronomer-cosmos

ENV DBT_PROFILES_DIR=/opt/airflow/dags/dbt/jaffle
