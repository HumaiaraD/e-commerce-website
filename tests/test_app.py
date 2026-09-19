import pytest
from server.app import app, items
from server.store import Inventory


@pytest.fixture(autouse=True)
def reset_data():
    items.clear()
    items.append(
        Inventory(1, "Coffee", 5.99, "Beverages", "001234", 10)
    )


def test_get_items():
    client = app.test_client()
    response = client.get("/inventory")

    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "Coffee"


def test_get_item():
    client = app.test_client()
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_item_not_found():
    client = app.test_client()
    response = client.get("/inventory/99")

    assert response.status_code == 404


def test_create_item():
    client = app.test_client()
    response = client.post("/inventory", json={
        "name": "Tea",
        "price": 3.99,
        "category": "Beverages",
        "barcode": "123456",
        "quantity": 5
    })

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Tea"
    assert len(items) == 2


def test_update_item():
    client = app.test_client()
    response = client.patch("/inventory/1", json={
        "price": 7.99,
        "quantity": 20
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 7.99
    assert data["quantity"] == 20
    assert data["name"] == "Coffee"


def test_update_item_not_found():
    client = app.test_client()
    response = client.patch("/inventory/99", json={"price": 2.99})

    assert response.status_code == 404


def test_delete_item():
    client = app.test_client()
    response = client.delete("/inventory/1")

    assert response.status_code == 204
    assert len(items) == 0


def test_delete_item_not_found():
    client = app.test_client()
    response = client.delete("/inventory/99")

    assert response.status_code == 404