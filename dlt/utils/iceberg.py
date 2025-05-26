import os
import re
from pyiceberg.catalog import load_catalog
import pyarrow.dataset as ds
import pyarrow.fs


def get_timestamp_from_path(file_path):
    match = re.search(r"\d+\.\d+", file_path)
    return match.group(0) if match else None


def get_generated_parquet_files(table_catalog, pipeline, table_name):
    load_info = pipeline.last_trace.last_load_info

    table_files = []
    for package in load_info.load_packages:
        for job in package.jobs["completed_jobs"]:
            if (
                job.job_file_info.table_name == table_name
                and job.job_file_info.file_format == "parquet"
            ):
                timestamp = get_timestamp_from_path(job.file_path)
                s3_path = f"{table_catalog}/{pipeline.dataset_name}/{table_name}/{timestamp}.{job.job_file_info.file_id}.parquet"
                table_files.append(s3_path)
    return table_files


def create_or_update_iceberg_table(
    table_catalog, table_schema, table_name, parquet_paths
):
    access_key = os.environ.get(
        "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"
    )
    secret_access_key = os.environ.get(
        "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
    )
    s3_endpoint = os.environ.get("DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL")
    region = os.environ.get("DESTINATION__FILESYSTEM__CREDENTIALS__REGION_NAME")
    catalog_uri = os.environ.get("PYICEBERG_CATALOG__LAKEKEEPER__URI")

    catalog = load_catalog(
        table_catalog,
        **{
            "uri": catalog_uri,
            "s3.endpoint": s3_endpoint,
            "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
            "s3.access-key-id": access_key,
            "s3.secret-access-key": secret_access_key,
        },
    )

    fs = pyarrow.fs.S3FileSystem(
        region=region,
        endpoint_override=s3_endpoint,
        scheme="http",
        access_key=access_key,
        secret_key=secret_access_key,
    )

    dataset = ds.dataset(parquet_paths, format="parquet", filesystem=fs)

    catalog.create_namespace_if_not_exists(table_schema)
    identifier = f"{table_schema}.{table_name}"

    if not catalog.table_exists(identifier):
        catalog.create_table(identifier, dataset.schema)

    table = catalog.load_table(identifier)

    with table.update_schema() as update:
        update.union_by_name(dataset.schema)

    table.append(dataset.to_table())
    print("added asset to catalog")
