class PositiveNumber:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} не может быть отрицательным")
        setattr(instance, self.name, value)


class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        cache_attr = f'_cached_{self.name}'
        if hasattr(instance, cache_attr):
            return getattr(instance, cache_attr)

        value = self.func(instance)
        setattr(instance, cache_attr, value)
        return value


if __name__ == '__main__':
    class Product:
        price = PositiveNumber('_price')

        def __init__(self, price, quantity):
            self.price = price
            self.quantity = quantity

        @CachedProperty
        def total_price(self):
            print("Вычисление total_value...")
            return self.price * self.quantity

        def invalidate_cache(self):
            # Сбросить кэш всех CachedProperty этого объекта
            for attr in list(self.__dict__):
                if attr.startswith("_cached_"):
                    delattr(self, attr)

        def __setattr__(self, name, value):
            self.invalidate_cache()
            return super().__setattr__(name, value)

    product = Product(1200, 5)
    print(product.total_price)
    print(product.total_price)
    print(product.__dict__)
    product.quantity = 25
    print(product.total_price)
    print(product.__dict__)
