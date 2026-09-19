from unittest.mock import patch

import pytest
import requests

from app import fetch_product


def test_fetch_product():
    fake_data = {
        "product": {
            "product_name": "Water",
            "brands": "Example Brand"
        }
    }

    with patch("app.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_data

        result = fetch_product("123456")

        assert result == fake_data
        assert mock_get.call_args.args[0].endswith(
            "/product/123456.json"
        )
        mock_get.return_value.raise_for_status.assert_called_once()


def test_fetch_product_http_error():
    with patch("app.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("403 Forbidden")
        )

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_product("123456")


def test_fetch_product_timeout():
    with patch("server.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(requests.exceptions.Timeout):
            fetch_product("123456")