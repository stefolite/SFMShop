import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ
from src.database.connection import get_connection


def create_order_with_acid(user_id, product_id, quantity, total):
    """Создание заказа с соблюдением всех ACID принципов"""
    with get_connection() as conn:
        # I - Isolation: установка уровня изоляции
        conn.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)

        try:
            with conn.cursor() as cur:
                # C - Consistency: проверка согласованности перед операциями
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                balance = cur.fetchone()[0]
                if balance < total:
                    raise ValueError("Недостаточно средств")

                cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
                product_quantity = cur.fetchone()[0]
                if product_quantity < quantity:
                    raise ValueError("Недостаточно товара на складе")

                # A - Atomicity: все операции в одной транзакции
                cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id", (user_id, total))
                order_id = cur.fetchone()[0]

                cur.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))
                cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (total, user_id))

                # C - Consistency: проверка согласованности после операций
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                new_balance = cur.fetchone()[0]
                if new_balance < 0:
                    raise ValueError("Баланс стал отрицательным")

                cur.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
                new_quantity = cur.fetchone()[0]
                if new_quantity < 0:
                    raise ValueError("Количество товара стало отрицательным")

                # D - Durability: COMMIT гарантирует запись на диск
                conn.commit()
                return order_id

        except Exception as e:
            # A - Atomicity: откат всех изменений при ошибке
            conn.rollback()
            print(f"Ошибка при создании заказа: {e}")
            raise
