import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # используем DATABASE_URL или формируем из отдельных переменных

_pool = None

async def init_db_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return _pool

async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

async def fetch_avg_salary_6m():
    # пример запроса — средняя за последние 6 месяцев
    async with _pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT ROUND(AVG(amount)::numeric, 2) FROM salaries WHERE date_paid >= CURRENT_DATE - INTERVAL '6 months';"
        )
    
# Получить список всех сотрудников
async def fetch_all_employees():
    async with _pool.acquire() as conn:
        rows = await conn.fetch("SELECT employee_id, first_name, last_name, email, phone FROM employees ORDER BY employee_id")
    return rows