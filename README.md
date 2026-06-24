# flaky-test-retry-mechanism-example
This example demonstrates how "flaky tests" can randomly pass or fail in a CI pipeline. It shows a simulated flaky external service and two tests: one that fails intermittently, and another that uses a retry mechanism to stabilize the test, effectively mitigating the flakiness. Run this example multiple times to observe the difference in stability.
