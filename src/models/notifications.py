from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotification(Notification):
    def send(self,  message: str):
        print(f"Email: {message}")


class SMSNotification(Notification):
    def send(self,  message: str):
        print(f"SMS: {message}")


def send_notifications(notifications: list[tuple[Notification, str]]):
    for notification, message in notifications:
        notification.send(message)


if __name__ == '__main__':
    notifications = [
        (EmailNotification(), "hey"),
        (SMSNotification(), "qq"),
        (EmailNotification(), "sup"),
        (SMSNotification(), "bonjour"),
        (SMSNotification(), "hello")
    ]

    send_notifications(notifications)
