"""Simple Lesk word-sense disambiguation using WordNet gloss overlap."""

import re

import nltk
from nltk.corpus import wordnet as wn


def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def lesk(sentence, ambiguous_word):
    try:
        senses = wn.synsets(ambiguous_word)
    except LookupError:
        nltk.download("wordnet", quiet=True)
        senses = wn.synsets(ambiguous_word)
    if not senses:
        return None

    context = words(sentence) - {ambiguous_word.lower()}
    return max(
        senses,
        key=lambda sense: len(
            context
            & words(
                " ".join(
                    [sense.definition()]
                    + sense.examples()
                    + [lemma.name().replace("_", " ") for lemma in sense.lemmas()]
                )
            )
        ),
    )


if __name__ == "__main__":
    sentence = "The fisherman sat on the river bank and watched the water."
    sense = lesk(sentence, "bank")
    if sense:
        print(sense.name())
        print(sense.definition())
    else:
        print("No WordNet senses found")
