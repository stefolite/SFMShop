import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password
        )
        return conn
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None


def add_product(conn, name, price, quantity):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s) RETURNING id, name, price, quantity;",
                (name, price, quantity)
            )
            print(f"Товар добавлен: {name}, {price}, {quantity}")
            return cursor.fetchone()


def get_all_products(conn):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products;")
            products = cursor.fetchall()
    return products


def delete_product(conn, product_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s RETURNING id;", (product_id, ))
            product = cursor.fetchone()
            if product:
                return True
            return False


def update_product_price(conn, product_id, new_price):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE products SET price = %s WHERE id = %s",
                (new_price, product_id)
            )
            print(f"Цена обновлена: {new_price}")


def create_user(conn, name, email):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email;",
                    (name, email)
                )
                print(f'Пользователь создан: {name}, {email}')
                return cursor.fetchone()
    except Error as e:
        print(f"Ошибка при создании пользователя: {e}")


def get_users(conn):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            return cursor.fetchall()


def get_user_by_id(conn, user_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE id = %s;",
                    (user_id, )
                )
                user = cursor.fetchone()
                return user if user else None
    except Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None


def get_product_by_id(conn, product_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM products WHERE id = %s;",
                    (product_id, )
                )
                product = cursor.fetchone()
                return product if product else None
    except Error as e:
        print(f"Ошибка при получении продукта: {e}")
        return None


def create_order(conn, user_id, total):
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id, user_id, total, created_at;",
                    (user_id, total)
                )
                order = cursor.fetchone()
                print(f'Заказ создан: {user_id=}, {total=}')
                return order
    except Error as e:
        print(f"Ошибка при создании заказа: {e}")


def get_user_orders(conn, user_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM orders WHERE user_id = %s",
                    (user_id, )
                )
                orders = cursor.fetchall()
                return orders
    except Error as e:
        print(f"Ошибка при получении заказов: {e}")
        return []


def update_product(conn, data, product_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE products "
                    "SET name = %s, price = %s, quantity = %s "
                    "WHERE id = %s "
                    "RETURNING id, name, price, quantity;",
                    (data.name, data.price, data.quantity, product_id)
                )
                return cursor.fetchone()
    except Error as e:
        print(f"Ошибка при изменении продукта: {e}")


# Файл src/database/connection.py
# import os
# import psycopg2
# from contextlib import contextmanager
# from dotenv import load_dotenv

# load_dotenv()

# DB_CONFIG = {
#     "host": os.getenv("DB_HOST", "localhost"),
#     "port": int(os.getenv("DB_PORT", 5432)),
#     "database": os.getenv("DB_NAME", "sfmshop"),
#     "user": os.getenv("DB_USER", "postgres"),
#     "password": os.getenv("DB_PASSWORD")
# }

@contextmanager
def get_connection():
    """Контекстный менеджер для подключения к БД"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Ошибка БД: {e}")
        raise
    finally:
        if conn:
            conn.close()

# def test_connection():
#     """Проверить подключение к БД"""
#     try:
#         with get_connection() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT version();")
#                 version = cur.fetchone()
#                 print(f"Подключение успешно! Версия: {version[0]}")
#     except Exception as e:
#         print(f"Ошибка подключения: {e}")

# if __name__ == "__main__":
#     test_connection()