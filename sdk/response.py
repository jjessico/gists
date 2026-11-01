"""A minimal Responses request: python response.py [prompt]."""

import sys

from common import MODEL, client


def main() -> None:
    prompt = " ".join(sys.argv[1:]) or "Explain what a decision rule is in one sentence."
    result = client().responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        instructions="Answer clearly and briefly.",
        input=prompt,
    )
    print(result.output_text or "(no text returned)")


if __name__ == "__main__":
    main()
