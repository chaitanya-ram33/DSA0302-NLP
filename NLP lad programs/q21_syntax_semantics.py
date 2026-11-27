"""Extract noun phrases with spaCy and look up their WordNet meanings."""

import nltk
import spacy
from nltk.corpus import wordnet as wn


def main():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError as error:
        raise SystemExit(
            "Install the spaCy English model with: "
            "python -m spacy download en_core_web_sm"
        ) from error

    sentence = "A curious student read a book about language."
    doc = nlp(sentence)
    try:
        wn.synsets("student")
    except LookupError:
        nltk.download("wordnet", quiet=True)

    for chunk in doc.noun_chunks:
        head = chunk.root.lemma_.lower()
        senses = wn.synsets(head, pos=wn.NOUN)
        meaning = senses[0].definition() if senses else "No noun definition found"
        print(f"Noun phrase: {chunk.text!r}; head: {head!r}; meaning: {meaning}")


if __name__ == "__main__":
    main()
