"""Retrieve WordNet synsets, definitions, and example sentences with NLTK."""

import nltk
from nltk.corpus import wordnet as wn


def main():
    try:
        synsets = wn.synsets("bank")
        if not synsets:
            raise LookupError("WordNet corpus contains no synsets")
    except LookupError:
        nltk.download("wordnet", quiet=True)
        synsets = wn.synsets("bank")

    for synset in synsets[:8]:
        print(f"{synset.name()} ({synset.pos()}): {synset.definition()}")
        examples = synset.examples()
        if examples:
            print("  Example:", examples[0])


if __name__ == "__main__":
    main()
