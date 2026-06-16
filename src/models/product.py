# from src.models.exceptions import NegativePriceError, InsufficientStockError, SFMShopException


# class Product:
#     def __init__(self, name, price, quantity):
#         self.name = name
#         if price < 0:
#             raise NegativePriceError('Цена не может быть отрицательной')
#         self.price = price
#         self.quantity = quantity

#     def sell(self, amount):
#         if self.quantity < amount:
#             raise InsufficientStockError(f'Товара недостаточно. На складе: {self.quantity}, требуется: {amount}')
#         self.quantity = self.quantity - amount

#     @classmethod
#     def create_object(cls, data):
#         if data:
#             obj = cls(data[1], int(data[2]), int(data[3]))
#             obj.id = data[0]
#             return obj
#         return None


from dataclasses import dataclass
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        self.percent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, price: float) -> float:
        return max(0, price - self.amount)


@dataclass
class Product:
    name: str
    price: float
    quantity: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError('Цена не может быть отрицательной')
        if self.quantity < 0:
            raise ValueError('Количество не может быть отрицательным')

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"], data["quantity"])

    @staticmethod
    def calculate_discount(price, discount_percent):
        return price * (1 - discount_percent / 100)

    def calculate_price(self, discount: DiscountStrategy = None):
        return discount.apply(self.price) if discount else self.price


if __name__ == '__main__':
    data = {"name": "Мышь", "price": 1800, "quantity": 5}
    obj = Product.from_dict(data)
    # print(obj)
    # print(Product.calculate_discount(obj.price, 10))
    print(obj.calculate_price(PercentDiscount(57
                                              )))
    print(obj.calculate_price(FixedDiscount(500)))
