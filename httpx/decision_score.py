"""A score decision with HTTPX: python httpx/decision_score.py [issue]."""

import json
import sys

from common import MODEL, post


def main() -> None:
    issue = " ".join(sys.argv[1:]) or "Export fails in Safari but works in Chrome."
    decision = post(
        "/decisions",
        {
            "model": MODEL,
            "input": issue,
            "questions": [
                {
                    "type": "score",
                    "name": "severity",
                    "instructions": "How severe is this issue for the affected user?",
                    "levels": [
                        {"label": "Cosmetic", "description": "Appearance only; no lost functionality."},
                        {"label": "Workaround available", "description": "A task fails, but another way works."},
                        {"label": "Fully blocked", "description": "A task fails with no workaround."},
                    ],
                }
            ],
        },
    )
    answer = decision["answers"][0]
    print(json.dumps(answer, indent=2))
    if answer["type"] == "score":
        print(f"Weighted severity (0–2): {answer['score']:.3f} (confidence: {answer['confidence']:.3f})")


if __name__ == "__main__":
    main()
