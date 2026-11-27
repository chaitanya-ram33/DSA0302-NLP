"""Rank documents for a query using TF-IDF and cosine similarity."""

import math
import re
from collections import Counter


def tokenize(text):
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def rank_documents(query, documents):
    document_tokens = [tokenize(document) for document in documents]
    query_tokens = tokenize(query)
    vocabulary = set(query_tokens)
    for tokens in document_tokens:
        vocabulary.update(tokens)

    document_frequency = {
        term: sum(term in set(tokens) for tokens in document_tokens)
        for term in vocabulary
    }

    def vector(tokens):
        counts = Counter(tokens)
        length = len(tokens)
        if not length:
            return {}
        return {
            term: (count / length)
            * (math.log((1 + len(documents)) / (1 + document_frequency[term])) + 1)
            for term, count in counts.items()
        }

    query_vector = vector(query_tokens)
    query_norm = math.sqrt(sum(value * value for value in query_vector.values()))
    scores = []
    for index, tokens in enumerate(document_tokens):
        document_vector = vector(tokens)
        document_norm = math.sqrt(sum(value * value for value in document_vector.values()))
        dot_product = sum(
            weight * document_vector.get(term, 0.0)
            for term, weight in query_vector.items()
        )
        score = (
            dot_product / (query_norm * document_norm)
            if query_norm and document_norm
            else 0.0
        )
        scores.append((index, score))
    return sorted(scores, key=lambda result: result[1], reverse=True)


if __name__ == "__main__":
    documents = [
        "Cats are small domesticated mammals and popular pets.",
        "Dogs are loyal animals often trained to help people.",
        "Information retrieval searches documents using a user query.",
    ]
    for index, score in rank_documents("search documents", documents):
        print(f"{score:.3f}  Document {index + 1}: {documents[index]}")
