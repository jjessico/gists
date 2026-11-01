"""A Chat Completions request with Requests: python requests/chat_completion.py [prompt]."""

import sys

from common import MODEL, post


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or "Explain what a decision rule is in one sentence."
    completion = post(
        "/chat/completions",
        {
            "model": MODEL,
            "reasoning_effort": "none",
            "messages": [
                {"role": "developer", "content": "Answer clearly and briefly."},
                {"role": "user", "content": prompt},
            ],
        },
    )
    print(completion["choices"][0]["message"]["content"] or "(no text returned)")


if __name__ == "__main__":
    main()
