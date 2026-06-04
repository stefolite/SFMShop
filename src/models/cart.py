class ShoppingCart():
    def __init__(self, products=None):
        self.products = products if products else []

    def __add__(self, product):
        new_cart = self.products.copy()
        new_cart.append(product)
        return ShoppingCart(new_cart)

    def __len__(self):
        return len(self.products)

    def __iter__(self):
        return iter(self.products)

    def __str__(self):
        return " ".join(self.products)


if __name__ == '__main__':
    products_1 = ['Клавиатура', 'Мышь', 'Ноутбук']
    cart_1 = ShoppingCart(products_1)
    for product in cart_1:
        print(product)
    print("Продуктов всего:", len(cart_1))

    cart_2 = cart_1 + 'Наушники'

    print(cart_1, cart_2, sep='\n')
