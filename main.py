import unittest
import random
import time
import functools

# --- Simulate a Flaky System/Operation ---
class ExternalService:
    """
    Simulates an external service that is sometimes unreliable.
    """
    def __init__(self, reliability_rate=0.7):
        self.reliability_rate = reliability_rate # e.g., 70% chance of success

    def call(self, data):
        """
        Simulates an API call or data processing.
        It might randomly fail or succeed, mimicking a flaky dependency.
        """
        # Simulate some work with variable delay
        time.sleep(0.01 + random.random() * 0.05)

        if random.random() < self.reliability_rate:
            # This branch simulates a successful operation
            print(f"    [Service] Successfully processed: {data}")
            return f"Processed: {data}"
        else:
            # This branch simulates an intermittent failure
            print(f"    [Service] Failed to process: {data} (Simulated intermittent error)")
            raise ConnectionError("Simulated intermittent connection error or timeout.")

# --- Flaky Test Mitigation Strategy (Retry Decorator) ---
def retry_flaky_test(retries=3, delay_sec=0.1):
    """
    A decorator to retry a test method if it fails due to flakiness.
    This helps stabilize CI pipelines against transient issues.
    """
    def decorator(test_method):
        @functools.wraps(test_method)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            for i in range(retries):
                try:
                    test_method(self, *args, **kwargs)
                    print(f"  ✅ Test '{test_method.__name__}' passed on attempt {i+1}/{retries}.")
                    return # Test passed, no need to retry further
                except Exception as e:
                    last_exception = e
                    print(f"  ❌ Test '{test_method.__name__}' failed on attempt {i+1}/{retries}. Retrying...")
                    time.sleep(delay_sec)
            # If all retries fail, re-raise the last exception
            raise last_exception
        return wrapper
    return decorator

# --- Test Suite ---
class TestExternalServiceReliability(unittest.TestCase):
    def setUp(self):
        # Initialize the flaky service for each test
        self.service = ExternalService(reliability_rate=0.7) # 70% success rate

    def test_flaky_operation_without_retry(self):
        """
        This test directly calls the flaky service.
        It will sometimes fail due to the simulated intermittent error,
        demonstrating the "ghost" of flaky CI tests.
        """
        print("\n--- Running test_flaky_operation_without_retry (EXPECTED TO BE FLAKY) ---")
        # This call might raise ConnectionError randomly
        result = self.service.call("test_data_A")
        self.assertIsNotNone(result)
        self.assertIn("Processed", result)

    @retry_flaky_test(retries=5, delay_sec=0.05)
    def test_flaky_operation_with_retry(self):
        """
        This test uses a retry mechanism to mitigate flakiness.
        It makes the CI pipeline more stable by retrying failures,
        effectively "chasing away the ghost" of intermittent test failures.
        """
        print("\n--- Running test_flaky_operation_with_retry (SHOULD BE MORE STABLE) ---")
        # This call is wrapped with retry logic
        result = self.service.call("test_data_B")
        self.assertIsNotNone(result)
        self.assertIn("Processed", result)

if __name__ == "__main__":
    print("--- Observing Flaky CI Tests and Mitigation ---")
    print("Run this script multiple times to observe:")
    print("1. 'test_flaky_operation_without_retry' failing randomly.")
    print("2. 'test_flaky_operation_with_retry' being much more stable due to retries.")
    print("----------------------------------------------")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
