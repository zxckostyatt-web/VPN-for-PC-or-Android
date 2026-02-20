from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import os
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 6577270673  # ← ВСТАВЬ СВОЙ TELEGRAM ID

# ===== ФАЙЛЫ =====
FILES = {
    "proxy": "proxy.txt",
    "shadow_txt": "shadowproxy66.txt",

    "sub1": "withe-list/sub1.txt",
    "sub2": "withe-list/sub2.txt",
    "best_sub3": "withe-list/best_sub3.txt",
    "sub4": "withe-list/sub4.txt",
    "sub5": "withe-list/sub5.txt",
    "sub6": "withe-list/sub6.txt",
    "sub8": "withe-list/sub8.txt",
    "sub9": "withe-list/sub9.txt",
    "sub10": "withe-list/sub10.txt",
    "sub11": "withe-list/sub11.txt",
    "sub12": "withe-list/sub12.txt",
    "sub13": "withe-list/sub13.txt",
    "sub14": "withe-list/sub14.txt",
    "sub15": "withe-list/sub15.txt",
    "sub16": "withe-list/sub16.txt",
    "white_all": "withe-list/white_all_server.txt",
}

# ===== ГЛАВНОЕ МЕНЮ =====
main_keyboard = ReplyKeyboardMarkup(
    [
        ["📂 Католог"],
        ["ℹ️ Информация", "📖 Инструкция"],
    ],
    resize_keyboard=True
)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "VPN / Proxy бот",
        reply_markup=main_keyboard
    )

# ===== АДМИН ПАНЕЛЬ =====
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("📂 Заменить файл", callback_data="admin_replace")],
        [InlineKeyboardButton("📊 Список файлов", callback_data="admin_list")]
    ]

    await update.message.reply_text(
        "Админ панель:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== ОБРАБОТКА ТЕКСТА =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📂 Католог":
        keyboard = [
            [InlineKeyboardButton("VPN", callback_data="vpn_menu")],
            [InlineKeyboardButton("Прокси", callback_data="proxy")],
            [InlineKeyboardButton("Белые списки", callback_data="white_menu")]
        ]

        await update.message.reply_text(
            "Выберите раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===== CALLBACK =====
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ===== VPN =====
    if data == "vpn_menu":
        keyboard = [
            [InlineKeyboardButton("shadowproxy66", callback_data="shadow_txt")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_catalog")]
        ]

        await query.edit_message_text(
            "VPN раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== БЕЛЫЕ СПИСКИ =====
    elif data == "white_menu":
        keyboard = [
            [InlineKeyboardButton("sub1", callback_data="sub1")],
            [InlineKeyboardButton("sub2", callback_data="sub2")],
            [InlineKeyboardButton("BEST-sub3", callback_data="best_sub3")],
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
            [InlineKeyboardButton("withe-all-server", callback_data="white_all")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_catalog")]
        ]

        await query.edit_message_text(
            "Белые списки:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== ОТПРАВКА СОДЕРЖИМОГО =====
    elif data in FILES:
        try:
            with open(FILES[data], "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                await query.message.reply_text("Файл пустой.")
            else:
                for i in range(0, len(content), 4000):
                    await query.message.reply_text(content[i:i+4000])

        except Exception as e:
            await query.message.reply_text(f"Ошибка: {e}")

    # ===== АДМИН =====
    elif data == "admin_list":
        if query.from_user.id != ADMIN_ID:
            return

        file_list = "\n".join(FILES.keys())
        await query.message.reply_text(f"Файлы:\n{file_list}")

    elif data == "admin_replace":
        if query.from_user.id != ADMIN_ID:
            return

        keyboard = [
            [InlineKeyboardButton(k, callback_data=f"replace_{k}")]
            for k in FILES.keys()
        ]

        await query.message.reply_text(
            "Выберите файл для замены:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("replace_"):
        if query.from_user.id != ADMIN_ID:
            return

        file_key = data.replace("replace_", "")
        context.user_data["replace_file"] = file_key

        await query.message.reply_text("Отправьте новый .txt файл")

    # ===== НАЗАД =====
    elif data == "back_catalog":
        keyboard = [
            [InlineKeyboardButton("VPN", callback_data="vpn_menu")],
            [InlineKeyboardButton("Прокси", callback_data="proxy")],
            [InlineKeyboardButton("Белые списки", callback_data="white_menu")]
        ]

        await query.edit_message_text(
            "Каталог:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ===== ПРИЁМ ФАЙЛА ОТ АДМИНА =====
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if "replace_file" not in context.user_data:
        return

    file_key = context.user_data["replace_file"]
    file_path = FILES[file_key]

    document = update.message.document
    file = await document.get_file()
    await file.download_to_drive(file_path)

    await update.message.reply_text(f"Файл {file_key} обновлён ✅")
    context.user_data.pop("replace_file")

# ===== ЗАПУСК =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(CallbackQueryHandler(handle_callback))

print("Бот запущен...")
app.run_polling()
