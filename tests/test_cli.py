from argparse import Namespace
from unittest.mock import patch

from server.cli import (
    add_item, list_items, update_item, delete_item, find_item
)

BASE_URL = "http://127.0.0.1:5001"


def test_add_item():
    args = Namespace(
        name="Tea",
        price=3.99,
        category="Beverages",
        barcode="123456",
        quantity=5
    )

    with patch("cli.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"id": 2}

        add_item(args)

        mock_post.assert_called_once_with(
            f"{BASE_URL}/inventory",
            json=vars(args),
            timeout=10
        )


def test_list_items(capsys):
    with patch("cli.requests.get") as mock_get:
        mock_get.return_value.json.return_value = [
            {"name": "Coffee"}
        ]

        list_items(Namespace())

        mock_get.assert_called_once_with(
            f"{BASE_URL}/inventory",
            timeout=10
        )
        assert "Coffee" in capsys.readouterr().out


def test_update_item():
    args = Namespace(id=1, price=7.99, quantity=None)

    with patch("cli.requests.patch") as mock_patch:
        update_item(args)

        mock_patch.assert_called_once_with(
            f"{BASE_URL}/inventory/1",
            json={"price": 7.99},
            timeout=10
        )


def test_delete_item(capsys):
    with patch("cli.requests.delete") as mock_delete:
        delete_item(Namespace(id=1))

        mock_delete.assert_called_once_with(
            f"{BASE_URL}/inventory/1",
            timeout=10
        )
        mock_delete.return_value.json.assert_not_called()
        assert "deleted successfully" in capsys.readouterr().out


def test_find_item():
    with patch("cli.requests.get") as mock_get:
        find_item(Namespace(barcode="123456"))

        mock_get.assert_called_once_with(
            f"{BASE_URL}/inventory/lookup",
            params={"barcode": "123456"},
            timeout=10
        )