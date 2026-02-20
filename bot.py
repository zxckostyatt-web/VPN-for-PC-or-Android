import os
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# НАСТРОЙКИ
# =========================

TOKEN = os.getenv("TOKEN")  # TOKEN берется из Render Environment
ADMIN_ID = 123456789  # <-- ВСТАВЬ СВОЙ TELEGRAM ID

# =========================
# ФАЙЛЫ
# =========================

FILES = {
    # VPN
    "shadowproxy66": "shadowproxy66.txt",

    # Прокси
    "proxy": "proxy.txt",

    # Белые списки
    "sub1": "sub1.txt",
    "sub2": "sub2.txt",
    "best-sub3": "best-sub3.txt",
    "sub4": "sub4.txt",
    "sub5": "sub5.txt",
    "sub6": "sub6.txt",
    "sub8": "sub8.txt",
    "sub9": "sub9.txt",
    "sub10": "sub10.txt",
    "sub11": "sub11.txt",
    "sub12": "sub12.txt",
    "sub13": "sub13.txt",
    "sub14": "sub14.txt",
    "sub15": "sub15.txt",
    "sub16": "sub16.txt",
    "withe-all-server": "withe-all-server.txt",
}

# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

main_keyboard = ReplyKeyboardMarkup(
    [
        ["📂 Каталог"],
        ["ℹ️ Информация", "📖 Инструкция"],
    ],
    resize_keyboard=True
)

# =========================
# СТАРТ
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋 Это сборник VPN.",
        reply_markup=main_keyboard
    )

# =========================
# ТЕКСТОВЫЕ СООБЩЕНИЯ
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📂 Каталог":
        keyboard = [
            [InlineKeyboardButton("VPN", callback_data="vpn_menu")],
            [InlineKeyboardButton("Прокси", callback_data="proxy")],
            [InlineKeyboardButton("Белые списки", callback_data="white_menu")],
        ]
        await update.message.reply_text(
            "Выберите раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif text == "ℹ️ Информация":
        await update.message.reply_text(
            "Выбирайте сервер с меньшим пингом (мс).\n"
            "Если н/а — сервер не работает."
        )

    elif text == "📖 Инструкция":
        await update.message.reply_text(
            "1. Скачать VPN утилиту\n"
            "2. Запустить\n"
            "3. Скопировать ссылку\n"
            "4. Вставить через Clipboard"
        )

# =========================
# CALLBACK КНОПКИ
# =========================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ===== VPN =====
    if data == "vpn_menu":
        keyboard = [
            [InlineKeyboardButton("shadowproxy66", callback_data="shadowproxy66")],
            [InlineKeyboardButton("⬅ Назад", callback_data="back_catalog")]
        ]
        await query.edit_message_text(
            "VPN раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== ПРОКСИ =====
    elif data == "proxy":
        await send_file_content(query, "proxy")

    # ===== БЕЛЫЕ СПИСКИ =====
    elif data == "white_menu":
        keyboard = [
            [InlineKeyboardButton("sub1", callback_data="sub1")],
            [InlineKeyboardButton("sub2", callback_data="sub2")],
            [InlineKeyboardButton("BEST-sub3", callback_data="best-sub3")],
            [InlineKeyboardButton("sub4", callback_data="sub4")],
            [InlineKeyboardButton("sub5", callback_data="sub5")],
            [InlineKeyboardButton("sub6", callback_data="sub6")],
            [InlineKeyboardButton("sub8", callback_data="sub8")],
            [InlineKeyboardButton("sub9", callback_data="sub9")],
            [InlineKeyboardButton("sub10", callback_data="sub10")],
            [InlineKeyboardButton("sub11", callback_data="sub11")],
            [InlineKeyboardButton("sub12", callback_data="sub12")],
            [InlineKeyboardButton("sub13", callback_data="sub13")],
            [InlineKeyboardButton("sub14", callback_data="sub14")],
            [InlineKeyboardButton("sub15", callback_data="sub15")],
            [InlineKeyboardButton("sub16", callback_data="sub16")],
            [InlineKeyboardButton("withe-all-server", callback_data="withe-all-server")],
            [InlineKeyboardButton("⬅ Назад", callback_data="back_catalog")]
        ]
        await query.edit_message_text(
            "Белые списки:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== НАЗАД =====
    elif data == "back_catalog":
        keyboard = [
            [InlineKeyboardButton("VPN", callback_data="vpn_menu")],
            [InlineKeyboardButton("Прокси", callback_data="proxy")],
            [InlineKeyboardButton("Белые списки", callback_data="white_menu")],
        ]
        await query.edit_message_text(
            "Выберите раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== ОТПРАВКА ФАЙЛА =====
    elif data in FILES:
        await send_file_content(query, data)


# =========================
# ФУНКЦИЯ ОТПРАВКИ ФАЙЛА
# =========================

async def send_file_content(query, key):
    try:
        with open(FILES[key], "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            await query.message.reply_text("Файл пустой.")
        else:
            await query.message.reply_text(content)

    except Exception as e:
        await query.message.reply_text(f"Ошибка: {e}")

# =========================
# АДМИН ПАНЕЛЬ
# =========================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Нет доступа.")
        return

    await update.message.reply_text("Админ панель активна.")

# =========================
# ЗАПУСК
# =========================

if not TOKEN:
    raise ValueError("TOKEN не найден! Добавь его в Render Environment.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_callback))

print("Бот запущен...")
app.run_polling()
