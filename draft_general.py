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


class Descriptor(ABC):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    @abstractmethod
    def __set__(self, instance, value):
        pass


class PositiveNumber(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError("Значение должно быть целым числом")
        if value < 1:
            raise ValueError("Число должно быть положительным")
        setattr(instance, self.name, value)
        return None


class NotNegativeNumber(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Значение должно быть числом")
        if value < 0:
            raise ValueError("Число должно быть неотрицательным")
        setattr(instance, self.name, value)
        return None


class AgeDescriptor(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError("Значение должно быть целым числом")
        if value < 18:
            raise ValueError("Возраст должен быть больше или равен 18")
        setattr(instance, self.name, value)
        return None


class EmailDescriptor(Descriptor):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("Значение должно быть строкой")
        if "@" not in value:
            raise ValueError("Email указан неверно")
        setattr(instance, self.name, value)
        return None


class User(LoggableMixin, SerializableMixin):
    user_id = PositiveNumber("_user_id")
    email = EmailDescriptor("_email")
    age = AgeDescriptor("_age")
    balance = NotNegativeNumber("_balance")

    def __init__(self, user_id, name, email, age, balance=0):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.balance = balance
        self.orders = []
        self.is_active = True
        self.log(f"Создан пользователь: {name}")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "balance": self.balance,
            "orders_count": len(self.orders),
            "is_active": self.is_active
        }


class NotificationService(ABC):
    @abstractmethod
    @staticmethod
    def send(message):
        pass


class EmailNotificationService(NotificationService):
    @staticmethod
    def send(message):
        print(f"Уведомление отправлено на Email: {message}")


class Database(ABC):
    @abstractmethod
    def save(self, user: User):
        pass


class MySQLDatabase(Database):
    def save(self, user: User):
        print(f"Информация о пользователе с id {user.user_id} сохранена в БД")


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


class UserCalculator:
    @staticmethod
    def calculate_total_spent(user: User) -> float:
        """Расчет общей потраченной суммы"""
        total = 0
        for order in user.orders:
            total += order.total
        return total

    @staticmethod
    def calculate_discount(user: User, discount: DiscountStrategy = None) -> float:
        """Рассчитать стоимость со скидкой"""
        total = UserCalculator.calculate_total_spent(user)
        return discount.apply(total) if discount else total


class UserValidator:
    @staticmethod
    def validate(user: User) -> bool:
        """Валидация пользователя"""
        if not user.name:
            raise ValueError("Имя не может быть пустым")
        if "@" not in user.email:
            raise ValueError("Email должен содержать @")
        if user.age < 18:
            raise ValueError("Пользователь должен быть старше 18 лет")
        if user.balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        return True


class UserService:
    """Сервис для обработки пользователей (DIP)"""
    def __init__(self, notification_service: NotificationService, database: Database):
        self.notification_service = notification_service
        self.database = database

    def register_user(self, user: User):
        """Регистрация пользователя"""
        UserValidator.validate(user)
        self.notification_service.send(f"Добро пожаловать, {user.name}!")
        self.database.save(user)

    def generate_user_report(self, user: User) -> str:
        """Генерация отчета о пользователе (SRP)"""
        total_spent = UserCalculator.calculate_total_spent(user)
        report = f"Пользователь: {user.name}\n"
        report += f"Email: {user.email}\n"
        report += f"Всего заказов: {len(user.orders)}\n"
        report += f"Потрачено: {total_spent}\n"
        return report
