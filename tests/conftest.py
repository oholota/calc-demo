def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        default=None,
        help="URL of a running app for the HTTP tests, e.g. http://127.0.0.1:8000",
    )
