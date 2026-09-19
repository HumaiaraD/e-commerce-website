import argparse
import requests
from store import Inventory

#add item function
def add_item(args):
    data = {
        "name": args.name,
        "price": args.price,
        "category": args.category,
        "barcode": args.barcode,
        "quantity": args.quantity,
    }

    response = requests.post("http://127.0.0.1:5001/inventory", json=data, timeout=10)
    response.raise_for_status()
    print(response.json())

#dispalying item function
def list_items(args):
    response = requests.get("http://127.0.0.1:5001/inventory", timeout=10)
    response.raise_for_status()
    print(response.json())

#update an item function
def update_item(args):
    data = {}
    if args.price is not None:
        data["price"] = args.price
    if args.quantity is not None:
        data["quantity"] = args.quantity
    if data == {}:
        print("Enter a price or quantity")
        return
    response = requests.patch(f"http://127.0.0.1:5001/inventory/{args.id}", json=data, timeout=10)
    response.raise_for_status()
    print(response.json())

#delete an item function
def delete_item(args):
    response = requests.delete(f"http://127.0.0.1:5001/inventory/{args.id}", timeout=10)
    response.raise_for_status()
    print("Item deleted successfully.")

#find an item function
def find_item(args):
    response = requests.get(f"http://127.0.0.1:5001/inventory/lookup", params={"barcode": args.barcode}, timeout=10)
    response.raise_for_status()
    print(response.json())


# adding parsers now
parser = argparse.ArgumentParser(description="Inventory CLI")
subparsers = parser.add_subparsers(required=True)

# adding an item parser
add_parser = subparsers.add_parser("add-item", help="Add an item to inventory")
add_parser.add_argument("name")
add_parser.add_argument("price", type=float)
add_parser.add_argument("category")
add_parser.add_argument("barcode")
add_parser.add_argument("quantity", type=int)

add_parser.set_defaults(func=add_item)

# displaying all items parser
list_parser = subparsers.add_parser("list-items")
list_parser.set_defaults(func=list_items)

# update an item parser
update_parser = subparsers.add_parser("update-item")
update_parser.add_argument("id", type=int)
update_parser.add_argument("--price", type=float)
update_parser.add_argument("--quantity", type=int)
update_parser.set_defaults(func=update_item)

# delete an item parser
delete_parser = subparsers.add_parser("delete-item")
delete_parser.add_argument("id", type=int)
delete_parser.set_defaults(func=delete_item)

# finding an item parser
find_parser = subparsers.add_parser("find-item")
find_parser.add_argument("barcode")
find_parser.set_defaults(func=find_item)


if __name__ == "__main__":
    args = parser.parse_args()

    args.func(args)


