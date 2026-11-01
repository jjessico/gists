"""Estimate whether a condition is true: python decision_predicate.py [message]."""

import sys

from common import MODEL, client


def main() -> None:
    message = " ".join(sys.argv[1:]) or "My invoice shows the same $49 charge twice."
    decision = client().decisions.create(
        model=MODEL,
        input=message,
        questions=[
            {
                "type": "predicate",
                "name": "reports_duplicate_charge",
                "instructions": "Does the message report that the customer was charged twice?",
            }
        ],
    )
    answer = decision.answers[0]
    print(answer.model_dump_json(indent=2))
    if answer.type == "predicate":
        print(f"Estimated probability: {answer.probability:.3f}")


if __name__ == "__main__":
    main()
