import time


DB_PRODUCTS = [
    {"id": 1, "name": "Клавиатура", "price": 2500},
    {"id": 2, "name": "Мышь", "price": 1200},
]
db_calls = 0


def get_all_products_from_db():
    global db_calls
    db_calls += 1
    return DB_PRODUCTS


class SimpleCache:
    """Учебная модель Redis: key-value хранилище в памяти с TTL."""

    def __init__(self):
        self._store = {}  # key -> (value, expire_at)

    def setex(self, key, ttl_seconds, value):
        self._store[key] = (value, time.monotonic() + ttl_seconds)

    def get(self, key):
        value = self._store.get(key)
        if value:
            if time.monotonic() > value[1]:
                self.delete(key)
                return None
        return value

    def delete(self, key):
        if key in self._store:
            del self._store[key]
        return None


cache = SimpleCache()


def get_cached_products():
    """Сначала кэш, при промахе — БД и запись в кэш."""
    value = cache.get("products:all")
    if value:
        print("HIT")
        return value[0]
    cache.setex("products:all", 1, get_all_products_from_db())
    print("MISS")
    return cache.get("products:all")


def invalidate_products_cache():
    cache.delete("products:all")


if __name__ == "__main__":
    get_cached_products()
    get_cached_products()
    invalidate_products_cache()
    get_cached_products()
    time.sleep(1.1)
    products = get_cached_products()
    print(f"Обращений к БД: {db_calls}")
    print(f"Товаров: {len(products)}")
