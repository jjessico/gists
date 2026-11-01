"""A predicate decision with HTTPX: python httpx/decision_predicate.py [message]."""

import json
import sys

from common import MODEL, post


def main() -> None:
    message = " ".join(sys.argv[1:]) or "My invoice shows the same $49 charge twice."
    decision = post(
        "/decisions",
        {
            "model": MODEL,
            "input": message,
            "questions": [
                {
                    "type": "predicate",
                    "name": "reports_duplicate_charge",
                    "instructions": "Does the message report that the customer was charged twice?",
                }
            ],
        },
    )
    answer = decision["answers"][0]
    print(json.dumps(answer, indent=2))
    if answer["type"] == "predicate":
        print(f"Estimated probability: {answer['probability']:.3f}")


if __name__ == "__main__":
    main()
