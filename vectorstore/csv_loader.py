from random import random
import pandas as pd
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
from pymilvus import DataType, MilvusClient

class EmbeddingGenerator:
    """Generates embeddings for textual data."""

    def __init__(self, dimension=1536):
        self.dimension = dimension
        self.emebeding_model = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    def generate(self, text):
        """Generates an embedding for the text."""
        return self.emebeding_model.embed_query(text=text)


class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()
        self.client = MilvusClient(uri="http://localhost:19530")

    def load_data(self):
        data = pd.read_csv(self.file_path)
        data = data[data["cat_level_2"] == "Laptopy"]
        print (data.shape, "shape")
        # data = data.head(10)
        self.fillna_type_compliant(data)
        return data

    @staticmethod
    def fillna_type_compliant(df):
        for column in df.columns:
            dtype = df[column].dtype
            if pd.api.types.is_integer_dtype(dtype):
                df[column] = df[column].fillna(0)
            elif pd.api.types.is_float_dtype(dtype):
                df[column] = df[column].fillna(0.0)
            elif pd.api.types.is_string_dtype(dtype):
                df[column] = df[column].fillna("missing-data")
            elif pd.api.types.is_bool_dtype(dtype):
                df[column] = df[column].fillna(False)

    # POD DODANIE 100k rekordów z zabezpieczeniem na szybko
    @staticmethod
    def _prepare_schema():
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=1536)
        return schema
    @staticmethod
    def _prepare_index():
        index_params = MilvusClient.prepare_index_params()
        index_params.add_index(field_name="embedding", index_type="AUTOINDEX", metric_type="L2")
        return index_params
    #------------------

    def prepare_data(
        self,
        embedding_generator: EmbeddingGenerator = EmbeddingGenerator(),
        embedding_field_name="long_description",
        exclude_fields=None,
    ):
        if exclude_fields is None:
            exclude_fields = ["id"]

        data_rows = []
        for _, row in self.data.iterrows():
            prepared_row = {}
            # print("WIERSZ: " ,row, "\n","-----------","\n")
            for column in self.data.columns:
                if column not in exclude_fields:
                    if column == embedding_field_name:
                        prepared_row["embedding"] = embedding_generator.generate(row[column])
                        prepared_row[column] = row[column]
                    else:
                        prepared_row[column] = row[column]
            data_rows.append(prepared_row)
        return data_rows


    def vector_store_creation(
        self,
        embedding_generator: EmbeddingGenerator = EmbeddingGenerator(),
        embedding_field_name="long_description",
        exclude_fields=None,
        collection_name=None,
    ):
        assert collection_name is not None, "Collection name must be provided"
        if exclude_fields is None:
            exclude_fields = ["id"]
        data_rows = []

        # POD DODANIE 100k rekordów z zabezpieczeniem na szybko
        self.client.create_collection(
            collection_name=collection_name,
            schema=self._prepare_schema(),
            index_params=self._prepare_index(),
        )
        #------------------

        for _, row in self.data.iterrows():
            prepared_row = {}
            for column in self.data.columns:
                if column not in exclude_fields:
                    if column == embedding_field_name:
                        prepared_row["embedding"] = embedding_generator.generate(row[column])
                        prepared_row[column] = row[column]
                    else:
                        prepared_row[column] = row[column]
            data_rows.append(prepared_row)
            if len(data_rows) == 100:
                print("100records")
            if len(data_rows) == 1000:
                print("Inserting 1000 records", len(data_rows))
                self.client.insert(collection_name="full_morele_pl", data=data_rows)
                data_rows = []
        if len(data_rows) > 0:
            print("Last insert", len(data_rows))
            self.client.insert(collection_name="full_morele_pl", data=data_rows)
        return data_rows
    

if __name__ == "__main__":
    print("Running the CSVLoader")
    csv_loader = CSVLoader("data/products_all.csv")
    # prepared_data = csv_loader.prepare_data()
    csv_loader.vector_store_creation(collection_name="laptopy_morele_pl")
    # Fix the printing function to nicely format the output
    import json
    # print(json.dumps(prepared_data, indent=2))
