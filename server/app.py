# app.py
from flask import Flask, jsonify, request
from store import Inventory

app = Flask(__name__)

items = [
    Inventory(1, "Coffee", 5.99, "Beverages", "001234")
]

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the inventory!"}), 200


@app.route("/inventory", methods=["GET"])
def get_items():
    return jsonify([item.to_display() for item in items]), 200


@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = next((item for item in items if item.id == id), None)

    if item is None:
        return jsonify({"error": "item not found"}), 404
    
    return jsonify(item.to_display()),200


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    new_id = max((item.id for item in items), default=0) + 1
    new_item = Inventory(
        new_id,
        data["name"],
        data["price"],
        data["category"],
        data["barcode"]
    )
    items.append(new_item)

    return jsonify(new_item.to_display()), 201


@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    data = request.get_json()
    item = next((item for item in items if item.id == id), None)

    if item is None:
        return jsonify({"error": "Not found"}), 404
    
    if "name" in data:
        item.name = data["name"]

    if "price" in data:
        item.price = data["price"]

    if "quantity" in data:
        item.quantity = data["quantity"]

    if "category" in data:
        item.category = data["category"]

    if "barcode" in data:
        item.barcode = data["barcode"]

    return jsonify(item.to_display()), 200

@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = next((item for item in items if item.id == id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    items.remove(item)

    return "", 204

if __name__ == "__main__":
    app.run(debug=True)