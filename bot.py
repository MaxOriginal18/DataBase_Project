import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Импортируем работу с БД
from db_async import init_db_pool, close_db_pool, fetch_avg_salary_6m, fetch_all_employees


# --- Команды и обработчики ---

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я аналитический бот. Задай мне вопрос о бизнесе 📊\n"
        "Команды:\n"
        "/salary_avg — средняя зарплата за последние 6 мес. \n"
        "/employees - список сотрудников"
    )

# Команда /salary_avg (работа с БД)
async def salary_avg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        avg = await fetch_avg_salary_6m()
        if avg is None:
            await update.message.reply_text("Нет данных о выплатах за последние 6 месяцев.")
        else:
            await update.message.reply_text(f"Средняя выплата за 6 мес.: {avg} (РУБ.)")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при получении данных: {e}")

# Команда /employee — список сотрудников
async def employee_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        employees = await fetch_all_employees()
        if not employees:
            await update.message.reply_text("Нет данных о сотрудниках.")
            return

        text = "👥 Список сотрудников:\n\n"
        for emp in employees:
            text += (
                f"ID: {emp['employee_id']}\n"
                f"Имя: {emp['first_name']} {emp['last_name']}\n"
                f"Email: {emp['email']}\n"
                f"Телефон: {emp['phone'] or '—'}\n"
                "------------------------\n"
            )

        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при получении списка сотрудников: {e}")

# Ответ на любое другое сообщение
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(
        f"Ты написал: {user_text}\n"
        "(позже я научусь связываться с БД и RAG 🤖)"
    )

# --- Основной запуск приложения ---
def main():
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("salary_avg", salary_avg))
    app.add_handler(CommandHandler("employees", employee_list))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")

    # Инициализируем пул БД перед запуском и корректно закрываем после
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db_pool())

    try:
        app.run_polling()
    finally:
        loop.run_until_complete(close_db_pool())

if __name__ == "__main__":
    main()