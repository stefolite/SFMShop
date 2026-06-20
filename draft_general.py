# Файл src/database/queries.py
import time
from src.database.connection import get_connection

def measure_index_performance(conn):
    with conn:
        with conn.cursor() as cur:
            # Тест 1: Поиск товара по названию
            print("Тест 1: Поиск товара по названию")

            # Без индекса
            start_time = time.perf_counter()
            cur.execute("SELECT * FROM products WHERE name = %s", ("Ноутбук",))
            result = cur.fetchone()
            time_without_index = time.perf_counter() - start_time

            # Создание индекса
            cur.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)")
            conn.commit()

            # С индексом
            start_time = time.perf_counter()
            cur.execute("SELECT * FROM products WHERE name = %s", ("Ноутбук",))
            result = cur.fetchone()
            time_with_index = time.perf_counter() - start_time

            print(f"  Без индекса: {time_without_index:.6f} сек")
            print(f"  С индексом: {time_with_index:.6f} сек")
            if time_with_index > 0:
                speedup = time_without_index / time_with_index
                print(f"  Ускорение: {speedup:.2f}x")

            # Тест 2: Поиск заказов по пользователю
            print("\nТест 2: Поиск заказов по пользователю")

            # Без индекса
            start_time = time.perf_counter()
            cur.execute("SELECT * FROM orders WHERE user_id = %s", (1,))
            results = cur.fetchall()
            time_without_index = time.perf_counter() - start_time

            # Создание индекса
            cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
            conn.commit()

            # С индексом
            start_time = time.perf_counter()
            cur.execute("SELECT * FROM orders WHERE user_id = %s", (1,))
            results = cur.fetchall()
            time_with_index = time.perf_counter() - start_time

            print(f"  Без индекса: {time_without_index:.6f} сек")
            print(f"  С индексом: {time_with_index:.6f} сек")
            if time_with_index > 0:
                speedup = time_without_index / time_with_index
                print(f"  Ускорение: {speedup:.2f}x")

if __name__ == "__main__":
    measure_index_performance()