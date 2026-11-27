"""Translate English text into French with Hugging Face Transformers."""

from transformers import pipeline


def main():
    translator = pipeline(
        "translation_en_to_fr",
        model="Helsinki-NLP/opus-mt-en-fr",
    )
    text = "Natural language processing helps computers understand text."
    result = translator(text, max_length=128)
    print(result[0]["translation_text"])


if __name__ == "__main__":
    main()
