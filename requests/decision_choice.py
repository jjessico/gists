"""A choice decision with Requests: python requests/decision_choice.py [message]."""

import json
import sys

from common import MODEL, post


def main() -> None:
    message = " ".join(sys.argv[1:]) or "My invoice shows a duplicate charge."
    decision = post(
        "/decisions",
        {
            "model": MODEL,
            "input": message,
            "questions": [
                {
                    "type": "choice",
                    "name": "support_queue",
                    "instructions": "Which support queue should handle this message?",
                    "choices": [
                        {"value": "billing", "description": "Payments, invoices, and refunds."},
                        {"value": "technical", "description": "Problems using the product."},
                        {"value": "account", "description": "Sign-in and account access."},
                        {"value": "other", "description": "Anything outside these categories."},
                    ],
                }
            ],
        },
    )
    answer = decision["answers"][0]
    print(json.dumps(answer, indent=2))
    if answer["type"] == "choice":
        print(f"Selected queue: {answer['choice']} (confidence: {answer['confidence']:.3f})")


if __name__ == "__main__":
    main()
