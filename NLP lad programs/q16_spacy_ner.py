"""Named Entity Recognition with spaCy's English model."""

import spacy


def main():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError as error:
        raise SystemExit(
            "spaCy model not found. Install it with: "
            "python -m spacy download en_core_web_sm"
        ) from error

    text = "Satya Nadella visited Paris in March 2024 to meet Microsoft employees."
    doc = nlp(text)
    for entity in doc.ents:
        print(f"{entity.text:20} {entity.label_:12} {spacy.explain(entity.label_)}")


if __name__ == "__main__":
    main()
