from abc import ABC, abstractmethod


class PositiveNumber:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 1:
            raise ValueError
        setattr(instance, self.name, value)


class LogMixin:
    def log(self, message):
        print(message)


class Order:
    def __init__(self, id, user):
        self.id = id
        self.cart = []
        self.user = user
        self.status = 'pending'

    def __len__(self):
        return len(self.cart)

    def __add__(self, product):
        self.cart.append(product)
        return self


class Payment(ABC):
    amount = PositiveNumber('_amount')
    
    def __init__(self, order, amount):
        self.order = order
        self.amount = amount


class CardPayment(Payment):
    def __init__(self, order, amount, card_number):
        super().__init__(order, amount)
        self.card_number = card_number


class PayPalPayment(Payment):
    def __init__(self, order, amount, address):
        super().__init__(order, amount)
        self.address = address



x = CardPayment(1, 1, 123)


        