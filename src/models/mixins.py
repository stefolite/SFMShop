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
