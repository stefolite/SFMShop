import json


class ValidatableMixin:
    def validate(self):
        return True

    def is_valid(self):
        try:
            self.validate()
            return True
        except ValueError:
            return False


class SerializableMixin:
    def to_json(self):
        return json.dumps({
            "class": self.__class__.__name__,
            "data": self.__dict__
        }, ensure_ascii=False)


class LoggableMixin:
    def log(self, message):
        class_name = self.__class__.__name__
        print(f"{class_name}: {message}")
