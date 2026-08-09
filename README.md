# Token Bucket Limiter

Model burst capacity and gradual token refill with a deterministic clock.

All bundled examples use synthetic data.

## Run

Requires Python 3.9 or later; no third-party packages or network access are needed.

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

Run these commands from this repository's directory. The demo can also be launched from any directory by passing the absolute path to `main.py`.

## How it works

A bucket starts with a configurable balance, refills at `refill_rate` tokens per second, and never exceeds `capacity`. A successful request subtracts its weight; a denied request keeps the available balance. `retry_after()` estimates when the requested weight can fit, returning infinity for an impossible request. All time-taking methods reject backwards movement and non-finite numbers.

Each operation uses O(1) time and space. The clock is supplied by the caller, so the demo and tests do not sleep.

## Reuse

```python
from main import TokenBucket

bucket = TokenBucket(capacity=3, refill_rate=0.5, initial_tokens=1)
assert bucket.consume(now=0)
assert not bucket.consume(now=1)
assert bucket.retry_after(now=1) == 1.0
assert bucket.consume(now=2)
```

## Demo behavior

The demo spends an initial burst, denies requests while the balance is low, then admits requests after refill. Times are synthetic seconds, independent of the current date.

## Boundaries

State is local to one object and is not synchronized across threads or processes. Floating-point arithmetic suits the demonstration but can have precision effects for extreme values. A retry estimate does not reserve future capacity. For a live integration, supply a monotonic clock and choose whether the limit applies per user, route, or service.

## Verification

`test_main.py` exercises boundary conditions, invalid inputs, and meaningful behavior specific to this implementation. The default demo is deterministic and completes without external services. See the collection's verification report for the recorded run; run the commands above to verify this repository independently.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
