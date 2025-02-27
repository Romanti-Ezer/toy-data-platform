import dlt
import argparse
from dlt.sources.filesystem import filesystem, read_csv

def stream_csv(table_name):
    data = filesystem(file_glob=f"{table_name}.csv") | read_csv()
    data.apply_hints(table_name=table_name)
    return data

def main(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="standard_filesystem_csv",
        destination="filesystem",
        dataset_name="movies",
    )

    load_info = pipeline.run(stream_csv(table_name),table_format="iceberg",write_disposition="append")

    print(load_info)
    print(pipeline.last_trace.last_normalize_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files into raw layer.")
    parser.add_argument("-d", "--dataset", type=str, help="Name of the dataset", required=True)
    args = parser.parse_args()

    main(args.dataset)