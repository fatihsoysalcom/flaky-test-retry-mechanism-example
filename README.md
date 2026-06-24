# Flaky Test Retry Mechanism Example

This example demonstrates how "flaky tests" can randomly pass or fail in a CI pipeline. It shows a simulated flaky external service and two tests: one that fails intermittently, and another that uses a retry mechanism to stabilize the test, effectively mitigating the flakiness. Run this example multiple times to observe the difference in stability.

## Language

`python`

## How to Run

Save the code as `main.py`.
Open your terminal or command prompt.
Run the script using: `python main.py`

## Original Article

This example accompanies the Turkish article: [Güvenli Yazılım Yuvası İnşa Etmek: Dalgalı CI Testlerinin Hayaletini Nasıl Kovarsınız?](https://fatihsoysal.com/blog/guvenli-yazilim-yuvasi-insa-etmek-dalgali-ci-testlerinin-hayaletini-nasil-kovarsiniz/).

## License

MIT — see [LICENSE](LICENSE).
