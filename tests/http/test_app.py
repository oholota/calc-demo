"""HTTP tests: talk to a running app (local server, container or cluster).

    pytest tests/http --base-url http://127.0.0.1:8000
"""
import pytest
import requests


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    url = pytestconfig.getoption("base_url")
    if not url:
        pytest.skip("HTTP tests need a running app: pass --base-url http://HOST:PORT")
    return url.rstrip("/")


def calc(base_url, expression):
    return requests.post(f"{base_url}/api/calc", json={"expression": expression}, timeout=5)


def test_health(base_url):
    response = requests.get(f"{base_url}/healthz", timeout=5)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_page_has_all_digit_buttons(base_url):
    response = requests.get(f"{base_url}/", timeout=5)
    assert response.status_code == 200
    for digit in range(10):
        assert f'data-key="{digit}"' in response.text


def test_static_files_are_served(base_url):
    # Catches a classic container mistake: collectstatic or WhiteNoise missing.
    response = requests.get(f"{base_url}/static/calculator/calc.js", timeout=5)
    assert response.status_code == 200
    assert "api/calc" in response.text


def test_calculation(base_url):
    response = calc(base_url, "2+3*4")
    assert response.status_code == 200
    assert response.json()["result"] == 14


def test_division_by_zero_is_a_client_error(base_url):
    response = calc(base_url, "1/0")
    assert response.status_code == 400
    assert response.json()["error"] == "Division by zero"


def test_code_injection_is_rejected(base_url):
    response = calc(base_url, "__import__('os').getcwd()")
    assert response.status_code == 400


def test_malformed_request(base_url):
    response = requests.post(f"{base_url}/api/calc", data="not json", timeout=5)
    assert response.status_code == 400
