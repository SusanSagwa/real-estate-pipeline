Real Estate Data Pipeline

An end-to-end ELT pipeline that ingests King County, WA house-sale data, loads it into a cloud data warehouse, transforms it into analytics-ready models, and serves it through an interactive dashboard. The pipeline is orchestrated on a daily schedule and includes automated data quality tests.

Business questions it answers

How are median home prices trending month over month?
Which ZIP codes are most expensive per square foot?
Which sales were priced furthest below their neighborhood median (a screening tool for potential deals)?

Architecture

Kaggle CSV → AWS S3 (raw files) → Snowflake RAW → dbt STAGING → dbt ANALYTICS → Streamlit dashboard, all orchestrated by Apache Airflow.

Tech stack

Storage: AWS S3
Warehouse: Snowflake
Transformation and testing: dbt (dbt-snowflake)
Orchestration: Apache Airflow (Astro CLI, running in Docker/Podman)
Visualization: Streamlit in Snowflake
Language: Python and SQL

How it works

Source files land in an S3 bucket (raw/ prefix).
An Airflow task runs COPY INTO to load new files into RAW.raw_house_sales. Snowflake's load history makes this idempotent, so reruns don't create duplicates.
dbt builds a typed staging view (dates parsed, numeric strings cast, bad values nulled safely) and two analytics tables: monthly ZIP-level prices and a deal-finder model.
dbt tests check for nulls in key columns after every run.
The Streamlit app reads the analytics tables.

Design decisions

Raw data is stored as text so a bad value never blocks ingestion; typing happens in staging.
Least-privilege access: a dedicated TRANSFORMER role and a service user with key-pair authentication, plus an IAM user scoped to a single S3 bucket.
Secrets are never committed. Keys are mounted into containers at runtime.

Known limitations

The dataset is a static historical snapshot (2014 to 2015), so incremental loading is demonstrated by adding new files rather than a live feed.
The deal finder uses price per square foot only and ignores condition, lot, and land value, so it is a screening tool, not a valuation.
