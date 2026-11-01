# GPT-6 Luna Python API examples

The same five tasks are implemented with three Python clients. Matching filenames make it easy to compare the request and response handling.

| Task | OpenAI SDK | HTTPX | Requests |
| --- | --- | --- | --- |
| Chat Completions text reply | [`sdk/chat_completion.py`](sdk/chat_completion.py) | [`httpx/chat_completion.py`](httpx/chat_completion.py) | [`requests/chat_completion.py`](requests/chat_completion.py) |
| Responses text reply | [`sdk/response.py`](sdk/response.py) | [`httpx/response.py`](httpx/response.py) | [`requests/response.py`](requests/response.py) |
| Duplicate-charge predicate | [`sdk/decision_predicate.py`](sdk/decision_predicate.py) | [`httpx/decision_predicate.py`](httpx/decision_predicate.py) | [`requests/decision_predicate.py`](requests/decision_predicate.py) |
| Support-queue choice | [`sdk/decision_choice.py`](sdk/decision_choice.py) | [`httpx/decision_choice.py`](httpx/decision_choice.py) | [`requests/decision_choice.py`](requests/decision_choice.py) |
| Severity score | [`sdk/decision_score.py`](sdk/decision_score.py) | [`httpx/decision_score.py`](httpx/decision_score.py) | [`requests/decision_score.py`](requests/decision_score.py) |

The SDK examples use typed methods and response objects. The HTTPX and Requests examples send JSON directly to the same API endpoints and parse the returned JSON. Each folder has a `common.py` for its client setup. Every script accepts optional text after its name; with no argument, it uses a built-in example.

## Setup

Use Python 3.10 or newer. From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in your environment or put `OPENAI_API_KEY=...` in `.env.local` in this directory. The scripts also check for `.env.local` inside their own folder. An exported environment variable takes precedence. The key files are ignored by `.gitignore`.

## Run and compare

From this directory, use the same prompt with each client:

```bash
python sdk/chat_completion.py "Explain a decision rule in one sentence."
python httpx/chat_completion.py "Explain a decision rule in one sentence."
python requests/chat_completion.py "Explain a decision rule in one sentence."
```

Replace `chat_completion.py` with any matching filename in the table. For example:

```bash
python sdk/decision_choice.py "I cannot sign in to my account."
python httpx/decision_choice.py "I cannot sign in to my account."
python requests/decision_choice.py "I cannot sign in to my account."
```

The Decisions examples call `POST /v1/decisions` with a shared `input` and one named question. A predicate returns a probability from 0 to 1. A choice returns one supplied value, probabilities for every value, and confidence. A score returns probabilities for ordered levels, confidence, and a probability-weighted average of level indices. With the three levels in these examples, the score ranges from 0 to 2. Each example prints the full answer and a short summary; a refusal appears in the full answer.

The HTTP examples use `raise_for_status()` so API errors fail visibly. The Responses examples collect all `output_text` blocks from message items because an `output` array may also contain other item types.

For production routing, use labeled examples to set thresholds and decide when to send results for review. The model's output alone should not authorize consequential actions. Use Responses with Structured Outputs when you need a custom JSON object or a written explanation, rather than one of the three Decisions answer types.

## Verification

On October 31, 2026, all 15 scripts compiled. The original five SDK examples completed live API calls using `openai` 3.41.0, and an SDK example was rerun successfully after moving it into `sdk/`. All ten HTTPX and Requests examples completed live API calls. The text examples returned the requested text; the Decisions examples identified a duplicate charge, selected the account queue for a sign-in issue, and assigned the highest severity to a fully blocked checkout. These representative checks do not establish accuracy across other messages.

## Captured API output

Run `python capture_outputs.py` from this directory to run all 15 examples and refresh the JSON files under [`output/`](output). Each file has the request method, URL, headers, and full JSON payload; the response status, headers, and full JSON payload; and the script's printed output. The output folders mirror `sdk/`, `httpx/`, and `requests/`. Authentication and cookie headers are redacted in the saved files.

On October 31, 2026, all 15 captured calls returned HTTP 200. The capture runner executes the existing example scripts and records their actual HTTP exchanges without changing their request code.

Run `python capture_outputs.py --benchmark` to make ten measured calls for each of the 15 examples. The full exchange and response time for every run are saved under [`output/iterations/`](output/iterations/). The [response-time table](output/response_times.md) includes all ten measurements plus mean, median, minimum, and maximum for each example; [response_times.csv](output/response_times.csv) has one row per call. The benchmark completed on October 31, 2026 with 150 HTTP 200 responses.

## Official OpenAI documentation

- [Decisions API](https://developers.openai.com/api/reference/resources/decisions/methods/create)
- [Responses text generation](https://developers.openai.com/api/docs/guides/text)
- [Chat Completions API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
- [GPT-6 Luna model](https://developers.openai.com/api/docs/models/gpt-6-luna)
