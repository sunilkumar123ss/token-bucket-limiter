"""A single-process token bucket with an explicitly supplied monotonic clock."""
import argparse
import json
import math


def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    return float(value)


class TokenBucket:
    def __init__(self, capacity, refill_rate, now=0.0, initial_tokens=None):
        self.capacity = finite(capacity, "capacity")
        self.refill_rate = finite(refill_rate, "refill_rate")
        self.updated_at = finite(now, "now")
        if self.capacity <= 0 or self.refill_rate < 0:
            raise ValueError("capacity must be positive and refill_rate nonnegative")
        self.tokens = self.capacity if initial_tokens is None else finite(initial_tokens, "initial_tokens")
        if not 0 <= self.tokens <= self.capacity:
            raise ValueError("initial_tokens must be between zero and capacity")

    def available(self, now):
        now = finite(now, "now")
        if now < self.updated_at:
            raise ValueError("clock must not move backwards")
        self.tokens = min(self.capacity, self.tokens + (now - self.updated_at) * self.refill_rate)
        self.updated_at = now
        return self.tokens

    def _amount(self, amount):
        amount = finite(amount, "amount")
        if amount <= 0:
            raise ValueError("amount must be positive")
        return amount

    def consume(self, now, amount=1.0):
        amount = self._amount(amount)
        self.available(now)
        if amount > self.tokens:
            return False
        self.tokens -= amount
        return True

    def retry_after(self, now, amount=1.0):
        amount = self._amount(amount)
        available = self.available(now)
        if amount <= available:
            return 0.0
        if amount > self.capacity or self.refill_rate == 0:
            return math.inf
        return (amount - available) / self.refill_rate
