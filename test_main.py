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







if __name__ == '__main__':
    unittest.main()
