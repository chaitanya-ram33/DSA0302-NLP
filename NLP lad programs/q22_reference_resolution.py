"""Resolve pronouns to the nearest preceding noun phrase (simple heuristic)."""

import spacy

PRONOUNS = {
    "he", "him", "his", "she", "her", "hers", "it", "its",
    "they", "them", "their", "theirs",
}


def resolve_references(text, nlp):
    doc = nlp(text)
    mentions = [
        (chunk.start, chunk.text)
        for chunk in doc.noun_chunks
        if chunk.root.pos_ not in {"PRON"}
    ]
    resolutions = []
    for token in doc:
        if token.lower_ in PRONOUNS:
            candidates = [mention for start, mention in mentions if start < token.i]
            resolutions.append((token.text, candidates[-1] if candidates else None))
    return resolutions


def main():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError as error:
        raise SystemExit(
            "Install the spaCy English model with: "
            "python -m spacy download en_core_web_sm"
        ) from error
    text = "Maya gave Alex a book because she thought he would enjoy it."
    for pronoun, referent in resolve_references(text, nlp):
        print(f"{pronoun} -> {referent or 'unresolved'}")
    print("This nearest-mention baseline does not model gender or number.")


if __name__ == "__main__":
    main()
