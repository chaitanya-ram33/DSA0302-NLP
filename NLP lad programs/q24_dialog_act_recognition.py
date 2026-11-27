"""Recognize basic dialog acts with transparent keyword/pattern rules."""

import re


def dialog_act(utterance):
    text = utterance.strip().lower()
    if re.match(r"^(hi|hello|hey)\b", text):
        return "greeting"
    if re.match(r"^(thanks|thank you)\b", text):
        return "thank"
    if text.endswith("?") or re.match(r"^(who|what|when|where|why|how|can|could|would)\b", text):
        return "question"
    if re.match(r"^(please\b|could you\b|would you\b)", text):
        return "request"
    if re.match(r"^(yes|yeah|yep|sure|okay|ok)\b", text):
        return "answer/affirmation"
    if re.match(r"^(no|nope|not really)\b", text):
        return "answer/negation"
    if re.match(r"^(bye|goodbye|see you)\b", text):
        return "goodbye"
    return "statement"


if __name__ == "__main__":
    conversation = [
        "Hello, how are you?",
        "Could you send me the report?",
        "Sure, I will send it today.",
        "Thank you!",
        "Goodbye.",
    ]
    for utterance in conversation:
        print(f"{dialog_act(utterance):20} {utterance}")
