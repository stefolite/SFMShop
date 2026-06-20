import json
import redis
from src.database.queries import get_all_products_from_db

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cached_products():
    """Получение товаров с кэшированием"""
    pass