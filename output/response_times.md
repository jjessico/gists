# API response times

Measured 2026-10-31T14:25:37+00:00 (UTC). Ten sequential runs per example, 150 calls total. Timing starts immediately before the client call and ends when the HTTP response returns. It includes connection setup and network time, but excludes Python process startup, JSON parsing, and file writing. Each run uses a fresh process.

All times are milliseconds. Individual exchanges are in [`iterations/`](iterations/); machine-readable timings are in [`response_times.csv`](response_times.csv).

| Client | Example | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Mean | Median | Min | Max |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sdk | chat_completion.py | 766.7 | 672.1 | 914.8 | 1311.3 | 643.8 | 963.7 | 925.7 | 817.0 | 682.2 | 871.9 | 856.9 | 844.4 | 643.8 | 1311.3 |
| sdk | response.py | 1095.4 | 1710.5 | 1000.2 | 1306.4 | 2220.8 | 964.1 | 2677.2 | 1125.8 | 1095.5 | 855.1 | 1405.1 | 1110.6 | 855.1 | 2677.2 |
| sdk | decision_predicate.py | 246.0 | 192.9 | 182.4 | 171.9 | 219.1 | 249.9 | 217.9 | 291.9 | 183.4 | 144.7 | 210.0 | 205.4 | 144.7 | 291.9 |
| sdk | decision_choice.py | 151.3 | 177.5 | 216.5 | 250.7 | 159.0 | 300.2 | 136.7 | 267.4 | 265.9 | 520.5 | 244.6 | 233.6 | 136.7 | 520.5 |
| sdk | decision_score.py | 235.4 | 312.7 | 217.4 | 146.2 | 351.6 | 147.1 | 312.2 | 564.0 | 155.8 | 246.6 | 268.9 | 241.0 | 146.2 | 564.0 |
| httpx | chat_completion.py | 636.7 | 684.9 | 737.2 | 609.4 | 932.3 | 686.3 | 587.3 | 1052.6 | 745.4 | 872.0 | 754.4 | 711.7 | 587.3 | 1052.6 |
| httpx | response.py | 887.9 | 903.8 | 971.4 | 1201.1 | 1184.0 | 1116.3 | 1252.9 | 1093.9 | 966.0 | 979.8 | 1055.7 | 1036.8 | 887.9 | 1252.9 |
| httpx | decision_predicate.py | 249.9 | 299.2 | 283.6 | 256.4 | 166.9 | 854.1 | 252.6 | 348.7 | 226.5 | 212.0 | 315.0 | 254.5 | 166.9 | 854.1 |
| httpx | decision_choice.py | 616.7 | 168.7 | 131.5 | 144.1 | 274.8 | 115.2 | 138.3 | 286.7 | 133.7 | 409.8 | 242.0 | 156.4 | 115.2 | 616.7 |
| httpx | decision_score.py | 150.1 | 226.4 | 228.2 | 143.0 | 214.8 | 223.3 | 139.0 | 242.0 | 369.5 | 294.0 | 223.0 | 224.8 | 139.0 | 369.5 |
| requests | chat_completion.py | 601.3 | 768.5 | 598.9 | 907.4 | 718.7 | 799.0 | 698.5 | 637.4 | 1006.9 | 966.9 | 770.4 | 743.6 | 598.9 | 1006.9 |
| requests | response.py | 1487.0 | 1033.6 | 983.4 | 1155.1 | 1042.3 | 811.8 | 1195.6 | 1080.4 | 852.2 | 1165.1 | 1080.6 | 1061.3 | 811.8 | 1487.0 |
| requests | decision_predicate.py | 130.0 | 230.2 | 199.5 | 164.1 | 310.2 | 240.5 | 155.3 | 219.3 | 235.2 | 253.8 | 213.8 | 224.8 | 130.0 | 310.2 |
| requests | decision_choice.py | 260.8 | 202.6 | 220.6 | 416.1 | 196.7 | 337.1 | 279.4 | 325.6 | 255.0 | 212.0 | 270.6 | 257.9 | 196.7 | 416.1 |
| requests | decision_score.py | 223.8 | 130.0 | 158.4 | 379.0 | 155.1 | 156.5 | 139.5 | 245.6 | 241.3 | 237.0 | 206.6 | 191.1 | 130.0 | 379.0 |
