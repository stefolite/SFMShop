from abc import ABC, abstractmethod
import json


class LoggableMixin:
    """Миксин для добавления функциональности логирования"""
    def log(self, message):
        class_name = self.__class__.__name__
        print(f"[{class_name}] {message}")


class SerializableMixin:
    """Миксин для добавления функциональности сериализации в JSON"""
    def to_dict(self):
        # Возвращает словарь атрибутов объекта
        return self.__dict__

    def to_json(self):
        # Сериализует объект в JSON строку
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)


class PositiveNumber:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Значение должно быть числом")
        if value < 1:
            raise ValueError("Число должно быть положительным")
        setattr(instance, self.name, value)


class Order(LoggableMixin, SerializableMixin):
    """Класс только для хранения данных заказа (SRP)"""
    user_id = PositiveNumber("_user_id")

    def __init__(self, user, products, order_id=None, created_at=None):
        self.user_id = user
        self.products = products
        self.order_id = order_id
        self.created_at = created_at
        self.log(f"Создан заказ: {order_id}")

    def calculate_total(self):
        """Удобная обёртка для обратной совместимости (делегирует в OrderCalculator)"""
        return OrderCalculator.calculate_total(self)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "products": [
                product.to_dict() if hasattr(product, "to_dict") else str(product)
                for product in self.products
            ],
            "order_id": self.order_id,
            "created_at": str(self.created_at) if self.created_at else None,
        }


class OrderValidator:
    """Класс для валидации заказа (SRP)"""
    @staticmethod
    def validate(order: Order) -> bool:
        if not order.products:
            raise ValueError("Заказ не может быть пустым")
        if not order.user_id:
            raise ValueError("Заказ должен иметь пользователя")
        return True


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


class NotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass


class EmailNotification(NotificationService):
    def send(self, order: Order):
        print(f"Отправка информации о заказе {order.order_id} на Email")


class Database(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass


class PostgreSQLDatabase(Database):
    def save(self, order: Order):
        print(f"Сохранение заказа {order.order_id} в PostgreSQL")


class OrderCalculator:
    """Класс для расчетов заказа (SRP)"""

    @staticmethod
    def calculate_total(order: Order) -> float:
        """Рассчитать общую стоимость заказа"""
        total = 0
        for product in order.products:
            total += product.get_total_price()
        return total

    @staticmethod
    def calculate_discount(order: Order, discount: DiscountStrategy = None) -> float:
        """Рассчитать стоимость со скидкой"""
        return discount.apply(order.calculate_total()) if discount else order.calculate_total()


class OrderService:
    """Сервис для обработки заказов (DIP)"""
    def __init__(self, notification_service: NotificationService, database: Database):
        self.notification_service = notification_service
        self.database = database

    def process_order(self, order: Order, discount: DiscountStrategy = None):
        """Обработка заказа"""
        OrderValidator.validate(order)
        total = OrderCalculator.calculate_total(order)
        if discount:
            total = OrderCalculator.calculate_discount(order, discount)
        self.notification_service.send(order)
        self.database.save(order)
        return total
