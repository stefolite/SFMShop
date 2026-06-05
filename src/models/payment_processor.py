from abc import ABC, abstractmethod


class Payment:
    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "pending"


class PaymentValidator(ABC):
    @staticmethod
    @abstractmethod
    def validate_payment():
        pass


class DefaultPaymentValidator(PaymentValidator):
    @staticmethod
    def validate_payment(payment):
        if payment.amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if isinstance(payment.payment_method, PaymentMethod):
            raise ValueError("Неизвестный метод оплаты")
        return True


class PaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment):
        pass


class PostgreSQLPaymentRepository(PaymentRepository):
    def save(self, payment: Payment):
        print(f"Сохранение платежа {payment.order_id} в PostgreSQL")


class NotificationService(ABC):
    @abstractmethod
    def send(self, payment: Payment):
        pass


class EmailNotification(NotificationService):
    def send(self, payment: Payment):
        print(f"Отправка информации о платеже {payment.order_id} на Email")


class PaymentMethod(ABC):
    @abstractmethod
    def calculate_fee(self, amount):
        pass

    @abstractmethod
    def process(self):
        pass


class CardPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return amount * 0.02 if amount > 10000 else amount * 0.03

    def process(self, amount):
        fee = self.calculate_fee(amount)
        print(f"Зарядка карты на сумму {amount + fee}")
        return True


class PayPalPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return amount * 0.035

    def process(self, amount):
        fee = self.calculate_fee(amount)
        print(f"Зарядка PayPal на сумму {amount + fee}")
        return True


class BankTransferPayment(PaymentMethod):
    def calculate_fee(self, amount):
        return 50

    def process(self, amount):
        fee = self.calculate_fee(amount)
        print(f"Банковский перевод на сумму {amount + fee}")
        return True


class PaymentProcessor:
    def __init__(self, validator, repository, notification_service):
        self.validator = validator
        self.repository = repository
        self.notification_service = notification_service

    def process_payment(self, payment):
        self.validator.validate_payment(payment)

        success = payment.payment_method.process(payment.amount)

        if success:
            payment.status = "completed"
        else:
            payment.status = "failed"
            raise ValueError(
                f"Ошибка обработки платежа методом "
                f"{type(payment.payment_method).__name__}"
            )

        self.repository.save(payment)

        self.notification_service.send(payment)

        return payment.status


if __name__ == "__main__":
    payment_processor = PaymentProcessor(
        DefaultPaymentValidator,
        PostgreSQLPaymentRepository(),
        EmailNotification()
    )
    payment = Payment(1, 1000, CardPayment())
    print(payment_processor.process_payment(payment))
