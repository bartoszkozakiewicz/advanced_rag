from pinecone_text.sparse import BM25Encoder
import random

def main():
    corpus = ["The quick brown fox jumps over the lazy dog",
          "The lazy dog is brown",
          "The fox is brown"]
    
    bm25 = BM25Encoder()
    bm25.fit(corpus)
    doc_sparse_vector = bm25.encode_documents("The brown fox is quick")
    query_sparse_vector = bm25.encode_queries("Which fox is brown?")
    # Konwersja list do słownika
    sparse_vector = dict(zip(query_sparse_vector['indices'], query_sparse_vector['values']))


    print("Sparse doc vector: ", doc_sparse_vector, "Sparse po zmianie vector: ", sparse_vector)
    return 1

def generate_sparse_vector(dimension: int, non_zero_count: int) -> dict:
    indices = random.sample(range(dimension), non_zero_count)
    values = [random.random() for _ in range(non_zero_count)]
    sparse_vector = {index: value for index, value in zip(indices, values)}
    print("VEKTORY: ",sparse_vector)
    return sparse_vector


if __name__ == "__main__":
    main()
    # generate_sparse_vector(100, 10)