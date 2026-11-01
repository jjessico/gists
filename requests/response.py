"""A Responses request with Requests: python requests/response.py [prompt]."""

import sys

from common import MODEL, post


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or "Explain what a decision rule is in one sentence."
    result = post(
        "/responses",
        {
            "model": MODEL,
            "reasoning": {"effort": "none"},
            "instructions": "Answer clearly and briefly.",
            "input": prompt,
        },
    )
    text = "".join(
        content["text"]
        for item in result["output"]
        if item["type"] == "message"
        for content in item["content"]
        if content["type"] == "output_text"
    )
    print(text or "(no text returned)")


if __name__ == "__main__":
    main()
