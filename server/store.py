# store.py

class Inventory:
    def __init__(self, id, name, price, category, barcode, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.barcode = barcode
        self.quantity = quantity


    def to_display(self):
        return {"id": self.id, "name": self.name, 
                "price": self.price,"category": self.category, 
                "barcode": self.barcode, "quantity": self.quantity,
                }



        