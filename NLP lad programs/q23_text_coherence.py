"""Estimate local text coherence using similarity between adjacent sentences."""

import re
from collections import Counter
from math import log, sqrt


def tokenize(sentence):
    return re.findall(r"\b[a-z]+\b", sentence.lower())


def cosine_similarity(left, right):
    left_counts = Counter(left)
    right_counts = Counter(right)
    shared = set(left_counts) & set(right_counts)
    dot = sum(left_counts[word] * right_counts[word] for word in shared)
    left_norm = sqrt(sum(value * value for value in left_counts.values()))
    right_norm = sqrt(sum(value * value for value in right_counts.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def coherence_score(text):
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]
    if len(sentences) < 2:
        return 0.0, []
    similarities = [
        cosine_similarity(tokenize(first), tokenize(second))
        for first, second in zip(sentences, sentences[1:])
    ]
    return sum(similarities) / len(similarities), similarities


if __name__ == "__main__":
    sample = (
        "The rain fell all evening. The storm flooded several streets. "
        "The city sent crews to clear the water."
    )
    score, adjacent_scores = coherence_score(sample)
    print("Adjacent sentence similarities:", [round(value, 3) for value in adjacent_scores])
    print(f"Average local coherence score: {score:.3f}")
