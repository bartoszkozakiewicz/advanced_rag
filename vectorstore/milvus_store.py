import logging
import time
from random import random

from pymilvus import DataType, MilvusClient

from vectorstore.csv_loader import CSVLoader

logging.basicConfig(level=logging.INFO)


class MilvusStoreWithClient:
    def __init__(self, client_uri: str = "http://localhost:19530", csv_file_path: str = "data/products.csv"):
        self.client = MilvusClient(uri=client_uri)
        self.csv_loader = CSVLoader(csv_file_path)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _prepare_schema():
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=128)
        return schema

    @staticmethod
    def _prepare_index():
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(field_name="embedding", index_type="AUTOINDEX", metric_type="L2")
        return index_params

    def make_collection(self, collection_name: str):
        self.client.create_collection(
            collection_name=collection_name,
            schema=self._prepare_schema(),
            index_params=self._prepare_index(),
        )

    def recreate_collection(self, collection_name: str):
        if self.client.has_collection(collection_name):
            logging.info(f"Dropping existing collection: {collection_name}")
            self.client.drop_collection(collection_name)
            while self.client.has_collection(collection_name):
                time.sleep(1)

        logging.info(f"Creating collection: {collection_name}")
        self.make_collection(collection_name)

    def insert_data_from_csv(self, collection_name: str):
        prepared_data = self.csv_loader.prepare_data()
        self.logger.info(f"Inserting {len(prepared_data)} records into collection")
        self.client.insert(collection_name=collection_name, data=prepared_data)
        time.sleep(5000)

    def search(
        self,
        collection_name: str,
        data: list = None,
        fixed_filter: str = None,
        limit: int = 100,
        output_fields: list = None,
        search_params: dict = None,
    ):

        if data is None:
            data = [random() for _ in range(128)]
        if fixed_filter is None:
            # example from milvus docs: filter='claps > 30 and reading_time < 10',
            fixed_filter = "cat_level_1 == 'Zabawki i dziecko'"
        if output_fields is None:
            output_fields = ["id", "price", "cat_level_5", "url"]

        return self.client.search(
            collection_name=collection_name,
            data=data,
            filter=fixed_filter,
            limit=limit,
            output_fields=output_fields,
            search_params=search_params,
        )


if __name__ == "__main__":
    # creating collection
    COLLECTION_NAME = "morele_pl"
    milvus_store = MilvusStoreWithClient(csv_file_path="data/products.csv")
    # use only when you want to create a new collection with the same name (data clearing)
    # milvus_store.recreate_collection(COLLECTION_NAME)
    # use otherwise
    # | for different websites it would be good idea to create a new collection for each website
    #milvus_store.make_collection(COLLECTION_NAME)
    # insert new data but be careful to no create too many duplicates
    #milvus_store.insert_data_from_csv(COLLECTION_NAME)
    milvus_store.search(COLLECTION_NAME)
