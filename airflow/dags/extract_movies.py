from __future__ import annotations

import os
from datetime import datetime

from airflow import models
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models.baseoperator import chain

DAG_ID = "extract_movies"

DATASETS = ["imdb_top_1000","meta_critic","netflix_titles"]

SOURCES__FILESYSTEM__BUCKET_URL="file://app/data"
DESTINATION__FILESYSTEM__BUCKET_URL="s3://raw"
DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL="http://minio:9000"
DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME="us-east-1"
DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID=os.environ.get("DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID")
DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY=os.environ.get("DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY")



with models.DAG(
    DAG_ID,
    schedule="@once",
    start_date=datetime(2025, 2, 1),
    catchup=False,
    tags=["movies", "full"],
) as dag:
    tasks = []
    for dataset in DATASETS: 
        task = DockerOperator(
            docker_url="unix://var/run/docker.sock", 
            image="my-dlt-pipeline:latest",
            command=["python","filesystem_pipeline.py","-d", dataset],
            network_mode="container:airflow_scheduler",
            task_id=f"ingestion-movies-{dataset}",
            auto_remove="force",
            dag=dag,
            environment={
                "SOURCES__FILESYSTEM__BUCKET_URL":SOURCES__FILESYSTEM__BUCKET_URL,
                "DESTINATION__FILESYSTEM__BUCKET_URL": DESTINATION__FILESYSTEM__BUCKET_URL,
                "DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL": DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL,
                "DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME": DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME,
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID": str(DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID),
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY": str(DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY)
            }
        )
        tasks.append(task)

chain(*tasks)
