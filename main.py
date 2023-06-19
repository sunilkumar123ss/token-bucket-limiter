"""A single-process token bucket with an explicitly supplied monotonic clock."""
import argparse
import json
import math


def finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(name + " must be a finite number")
    return float(value)
