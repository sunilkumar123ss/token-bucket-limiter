import math
import unittest
from main import TokenBucket


class TokenBucketTests(unittest.TestCase):
    def test_initial_burst_then_denial(self):
        bucket = TokenBucket(2, 1)
        self.assertTrue(bucket.consume(0))
        self.assertTrue(bucket.consume(0))
        self.assertFalse(bucket.consume(0))

    def test_fractional_refill_and_weight(self):
        bucket = TokenBucket(3, 0.5, initial_tokens=0)
        self.assertFalse(bucket.consume(1))
        self.assertTrue(bucket.consume(3, 1.5))
        self.assertEqual(bucket.tokens, 0)

    def test_refill_is_capped(self):
        bucket = TokenBucket(2, 1, initial_tokens=0)
        self.assertEqual(bucket.available(100), 2)

    def test_denial_does_not_debit(self):
        bucket = TokenBucket(3, 1, initial_tokens=1)
        self.assertFalse(bucket.consume(0, 2))
        self.assertEqual(bucket.tokens, 1)
        self.assertEqual(bucket.retry_after(0, 2), 1)

    def test_impossible_request(self):
        self.assertTrue(math.isinf(TokenBucket(2, 1).retry_after(0, 3)))
        self.assertTrue(math.isinf(TokenBucket(2, 0, initial_tokens=0).retry_after(0)))

    def test_clock_reversal_rejected_without_mutation(self):
        bucket = TokenBucket(2, 1, now=4)
        with self.assertRaises(ValueError):
            bucket.consume(3)
        self.assertEqual(bucket.available(4), 2)



if __name__ == '__main__':
    unittest.main()
