from typing import Any
from google.cloud import bigquery
import pandas as pd

from constants import GcpConstants


def bq_download_as_dataframe(
        project: str = GcpConstants.project.value,
        dataset_id: str = GcpConstants.dataset_id_all.value,
        table_name: str = GcpConstants.AllDataPivot.name
) -> pd.DataFrame:
    """
    Download whole table as Pandas DataFrame

    :param project: Project name
    :param dataset_id: Dataset ID
    :param table_name: Table Name
    :return: Table as pd.DataFrame
    """
    client = bigquery.Client()

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = dataset_ref.table(table_name)
    table = client.get_table(table_ref)
    return client.list_rows(table).to_dataframe()

def bq_run_query(
        query: str,
        project: str = GcpConstants.project.value,
        dataset_id: str = GcpConstants.dataset_id_all.value,
        table_name: str = GcpConstants.AllDataPivot.name,
) -> bigquery.job.QueryJob:
    """
    Run SQL query against BigQuery table

    :param query: SQL query to run
    :param project: Project name
    :param dataset_id: Dataset ID
    :param table_name: Table Name
    :return: Results of query
    """
    # Construct a BigQuery client object.
    client = bigquery.Client()

    query_job = client.query(query)  # Make an API request.

    return query_job

