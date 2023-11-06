import math
import unittest
from main import TokenBucket


class TokenBucketTests(unittest.TestCase):
    def test_initial_burst_then_denial(self):
        bucket = TokenBucket(2, 1)
        self.assertTrue(bucket.consume(0))
        self.assertTrue(bucket.consume(0))
        self.assertFalse(bucket.consume(0))








if __name__ == '__main__':
    unittest.main()
