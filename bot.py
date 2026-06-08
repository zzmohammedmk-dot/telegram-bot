import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8632097893:AAEsxoWe7OVIdncvK1KdsQ45S2pjtgdTGIY"

EXCEL_FILE = "prices.xlsx"

df = pd.read_excel(EXCEL_FILE)
CATEGORY_COL = "صنف"
SERVICE_COL = "الخدمة"
PRICE_COL = "السعر بالدينار العراقي - جديد 2026"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = sorted(
        df[CATEGORY_COL].dropna().astype(str).unique()
    )

    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"cat:{cat}")]
        for cat in categories
    ]

    await update.message.reply_text(
        "اختر الصنف:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("cat:"):
        cat = query.data[4:]

        services = (
            df[df[CATEGORY_COL].astype(str) == cat][SERVICE_COL]
            .dropna()
            .astype(str)
            .tolist()
        )

        context.user_data["services"] = services

        keyboard = [
            [InlineKeyboardButton(s, callback_data=f"srv:{i}")]
            for i, s in enumerate(services)
        ]

        await query.edit_message_text(
            f"الصنف: {cat}\n\nاختر الخدمة:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data.startswith("srv:"):
        idx = int(query.data[4:])
        service = context.user_data["services"][idx]

        row = df[df[SERVICE_COL].astype(str) == service].iloc[0]

        await query.edit_message_text(
            f"الخدمة:\n{service}\n\nالسعر:\n{row[PRICE_COL]}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()