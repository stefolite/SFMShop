class ModelMeta(type):
    _registry = {}

    def __new__(cls, name, bases, attrs):
        def to_dict(self):
            return self.__dict__

        attrs['to_dict'] = to_dict
        new_class = super().__new__(cls, name, bases, attrs)

        if name != 'Model':
            cls._registry[name] = new_class
        return new_class


class Product(metaclass=ModelMeta):
    pass


class Order(metaclass=ModelMeta):
    pass


class User(metaclass=ModelMeta):
    pass


if __name__ == '__main__':
    product = Product()
    product.id = 1
    print(product.to_dict())
    print(ModelMeta._registry)
