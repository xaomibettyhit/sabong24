import os
import sqlite3
import logging
from datetime import datetime

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

from data import ACTRESSES, CATEGORIES

# ---------- Configuration ----------
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DB_PATH = "actress.db"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def db_exec(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    r = c.fetchall()
    conn.close()
    return r

def add_user(user):
    db_exec(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, joined_at) VALUES (?,?,?,?)",
        (user.id, user.username or "", user.first_name or "", datetime.utcnow().isoformat())
    )

# ---------- Main Menu ----------
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Search Actress", callback_data="search_help")],
        [InlineKeyboardButton("📂 Browse by Category", callback_data="browse_categories")],
        [InlineKeyboardButton("🎬 Random Actress", callback_data="random_actress")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about_bot")],
    ])

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user)

    await update.message.reply_text(
        f"👋 Welcome to <b>Hollywood Actress Info</b>, {user.first_name}!\n\n"
        "Search any actress by name to see her profile, notable films, awards, "
        "and career highlights.\n\n"
        "You can also browse by category or discover someone new.\n\n"
        "Use the menu below to get started.",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

# ---------- Search Help ----------
async def search_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "🔍 <b>Search Actress</b>\n\n"
        "Just type the name of any actress in the chat, for example:\n\n"
        "• <code>Meryl Streep</code>\n"
        "• <code>Emma Stone</code>\n"
        "• <code>Zendaya</code>\n\n"
        "I'll send you her profile instantly.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ])
    )

# ---------- Browse Categories ----------
async def browse_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    keyboard = []
    for cat in CATEGORIES:
        keyboard.append([InlineKeyboardButton(f"📂 {cat}", callback_data=f"cat_{cat}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])
    await q.edit_message_text(
        "📂 <b>Browse by Category</b>\n\nChoose a category:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- Show Category ----------
async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cat = q.data.replace("cat_", "")
    matches = [a for a in ACTRESSES.values() if a["category"] == cat]

    if not matches:
        await q.edit_message_text("No actresses in this category yet.")
        return

    text = f"📂 <b>{cat}</b>\n\n"
    for a in matches:
        text += f"• {a['name']}\n"

    text += "\nType any name to see the full profile."

    await q.edit_message_text(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="browse_categories")]
        ])
    )

# ---------- Random Actress ----------
async def random_actress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    import random
    key = random.choice(list(ACTRESSES.keys()))
    await send_profile(q, key)

# ---------- Search Handler (text messages) ----------
async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    # Direct match
    if text in ACTRESSES:
        await send_profile(update, text)
        return

    # Partial match
    matches = [k for k in ACTRESSES if text in k]
    if len(matches) == 1:
        await send_profile(update, matches[0])
        return
    elif len(matches) > 1:
        keyboard = [[InlineKeyboardButton(ACTRESSES[k]["name"], callback_data=f"profile_{k}")] for k in matches]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])
        await update.message.reply_text(
            "Multiple matches found. Choose one:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "❌ I couldn't find that actress.\n\n"
        "Try another name, or use the menu to browse by category.",
        reply_markup=main_menu_keyboard()
    )

# ---------- Send Profile ----------
async def send_profile(target, key):
    a = ACTRESSES[key]
    text = (
        f"🎬 <b>{a['name']}</b>\n\n"
        f"📅 <b>Born:</b> {a['birth']}\n"
        f"🌍 <b>Nationality:</b> {a['nationality']}\n"
        f"🏷️ <b>Category:</b> {a['category']}\n\n"
        f"🎥 <b>Notable Films:</b>\n"
        + "\n".join(f"• {f}" for f in a["notable_films"])
        + f"\n\n🏆 <b>Awards:</b>\n"
        + "\n".join(f"• {aw}" for aw in a["awards"])
        + f"\n\n📝 <b>Bio:</b>\n{a['bio']}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Another Random", callback_data="random_actress")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="back")]
    ])

    if hasattr(target, "edit_message_text"):
        await target.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await target.message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)

# ---------- Profile Callback ----------
async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    key = q.data.replace("profile_", "")
    if key in ACTRESSES:
        await send_profile(q, key)

# ---------- About ----------
async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "ℹ️ <b>About Hollywood Actress Info</b>\n\n"
        "This bot is a lookup tool for fans of Hollywood cinema. "
        "Search any actress by name to see her profile, notable films, awards, "
        "and career milestones.\n\n"
        "No external links. No spam. Just useful film industry information.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ])
    )

# ---------- Back to Main Menu ----------
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "Main menu — choose an option:",
        reply_markup=main_menu_keyboard()
    )

# ---------- Main ----------
def main():
    if not BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN environment variable is required.")

    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Callbacks
    app.add_handler(CallbackQueryHandler(search_help, pattern="^search_help$"))
    app.add_handler(CallbackQueryHandler(browse_categories, pattern="^browse_categories$"))
    app.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(random_actress, pattern="^random_actress$"))
    app.add_handler(CallbackQueryHandler(profile_callback, pattern="^profile_"))
    app.add_handler(CallbackQueryHandler(about_bot, pattern="^about_bot$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))

    # Text search
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))

    logger.info("Hollywood Actress Info bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
