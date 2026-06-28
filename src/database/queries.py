import psycopg2


def get_orders_with_products(conn, user_id):
    """Получить заказы пользователя с товарами"""
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "orders.id, products.name, "
                "order_items.quantity, order_items.price "
                "FROM orders "
                "INNER JOIN order_items ON orders.id = products.order_id "
                "INNER JOIN products ON order_items.product_id = products.id "
                "WHERE orders.user_id = %s;",
                (user_id, )
            )
            orders = cursor.fetchall()
            return orders


def get_order_statistics(conn):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "users.id, "
                "users.name,"
                "COUNT(orders.id) as order_count,"
                "COALESCE(SUM(orders.total), 0) as total_sum "
                "FROM users "
                "LEFT JOIN orders ON users.id = orders.user_id "
                "GROUP BY users.id, users.name "
                "ORDER BY total_sum DESC;"
            )
            order_statistics = cursor.fetchall()
            return order_statistics


def get_user_order_history(conn, user_id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "orders.id, orders.created_at, products.name, "
                "order_items.quantity, order_items.price "
                "FROM orders "
                "INNER JOIN order_items "
                "ON orders.id = order_items.order_id"
                "INNER JOIN products "
                "ON order_items.product_id = products.id "
                "WHERE orders.user_id = %s "
                "ORDER BY orders.created_at DESC;",
                (user_id, )
            )
            order_history = cursor.fetchall()
            return order_history


def get_top_products(conn, limit=5):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT "
                "products.name, "
                "SUM(order_items.quantity) AS total_sold"
                "FROM products "
                "INNER JOIN order_items "
                "ON products.id = order_items.product_id"
                "GROUP BY products.name "
                "ORDER BY total_sold DESC "
                "LIMIT %s;",
                (limit, )
            )
            top_products = cursor.fetchall()
            return top_products



from psycopg2.extensions import (
    ISOLATION_LEVEL_READ_COMMITTED,
    ISOLATION_LEVEL_REPEATABLE_READ,
    ISOLATION_LEVEL_SERIALIZABLE
)


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

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


def read_user_balance(user_id):
    with get_connection() as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
        with conn.cursor() as cur:
            cur.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else 0


def calculate_total_revenue(start_date, end_date):
    with get_connection() as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_REPEATABLE_READ)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(SUM(total), 0) FROM orders WHERE created_at BETWEEN %s AND %s",
                (start_date, end_date)
            )
            total = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM orders WHERE created_at BETWEEN %s AND %s",
                (start_date, end_date)
            )
            count = cur.fetchone()[0]

            return {
                "total": float(total),
                "count": count,
                "average": float(total) / count if count > 0 else 0
            }


def critical_financial_operation(from_user_id, to_user_id, amount):
    with get_connection() as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)
        with conn.cursor() as cur:
            cur.execute("SELECT balance FROM users WHERE id = %s", (from_user_id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError("Пользователь не найден")
            balance = row[0]

            if balance < amount:
                raise ValueError("Недостаточно средств")

            cur.execute(
                "UPDATE users SET balance = balance - %s WHERE id = %s",
                (amount, from_user_id)
            )

            cur.execute(
                "UPDATE users SET balance = balance + %s WHERE id = %s",
                (amount, to_user_id)
            )

            return True
