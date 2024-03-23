from random import random

import pandas as pd


class EmbeddingGenerator:
    """Generates embeddings for textual data."""

    def __init__(self, dimension):
        self.dimension = dimension

    def generate(self, text):
        """Generates an embedding for the text."""
        return [random() for _ in range(self.dimension)]


class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        data = pd.read_csv(self.file_path)
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

    def prepare_data(
        self,
        embedding_generator: EmbeddingGenerator = EmbeddingGenerator(128),
        embedding_field_name="long_description",
        exclude_fields=None,
    ):
        if exclude_fields is None:
            exclude_fields = ["id"]

        data_rows = []

        for _, row in self.data.iterrows():
            prepared_row = {}
            for column in self.data.columns:
                if column not in exclude_fields:
                    if column == embedding_field_name:
                        prepared_row["embedding"] = embedding_generator.generate(row[column])
                    else:
                        prepared_row[column] = row[column]
            data_rows.append(prepared_row)

        return data_rows


if __name__ == "__main__":
    csv_loader = CSVLoader("data/products.csv")
    prepared_data = csv_loader.prepare_data()
    # Fix the printing function to nicely format the output
    import json

    print(json.dumps(prepared_data, indent=2))
