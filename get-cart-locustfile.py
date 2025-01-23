import json
from typing import List

import products
from cart import dao
from products import Product

class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in data['contents']],
            cost=data['cost']
        )

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])
        except json.JSONDecodeError:
            continue

        for product_id in contents:
            product = products.get_product(product_id)
            if product:
                items.append(product)

    return items

def add_to_cart(username: str, product_id: int):
    product = products.get_product(product_id)
    if product:
        dao.add_to_cart(username, product_id)
    else:
        raise ValueError(f"Product with ID {product_id} does not exist.")

def remove_from_cart(username: str, product_id: int):
    product = products.get_product(product_id)
    if product:
        dao.remove_from_cart(username, product_id)
    else:
        raise ValueError(f"Product with ID {product_id} does not exist.")

def delete_cart(username: str):
    dao.delete_cart(username)
