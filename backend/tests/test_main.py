from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_words_counter_valid_input():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "hello world"}
    )
    assert response.status_code == 200
    assert response.json() == {"words_count": 2}


def test_words_counter_empty_string():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "    "}
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Input string is empty or contains only whitespace."}


def test_words_counter_mixed_input():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "  hello    world  "}
    )
    assert response.status_code == 200
    assert response.json() == {"words_count": 2}


def test_words_counter_single_word():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "hello"}
    )
    assert response.status_code == 200
    assert response.json() == {"words_count": 1}


def test_words_counter_special_characters():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "hello, world!"}
    )
    assert response.status_code == 200
    assert response.json() == {"words_count": 2}


def test_words_counter_numerics():
    response = client.post(
        "/api/v1/words-counter",
        json={"words_string": "123 456"}
    )
    assert response.status_code == 200
    assert response.json() == {"words_count": 2}