### Inventory Management App

A Python inventory management app with a Flask REST API and an argparse CLI. Users can add, view, update, and delete inventory items, and look up food product details by barcode using Open Food Facts.

# Built With

Python, Flask, requests, argparse, pytest, and unittest.mock.

#Run

Install dependencies and start the API from the project folder:

pipenv install --dev
pipenv run python -m server.app

# In another terminal, use the CLI:

pipenv run python -m server.cli add-item "Coffee" 5.99 "Beverages" "001234" 10
pipenv run python -m server.cli list-items
pipenv run python -m server.cli update-item 1 --price 6.99 --quantity 20
pipenv run python -m server.cli delete-item 1
pipenv run python -m server.cli find-item 3274080005003

# Tests
My tests are not good enough

pipenv run python -m pytest tests -v

Inventory is stored in a temporary Python list and resets when the server restarts. Product lookup displays external details without automatically adding them to inventory.