import imaplib
import email
from email.header import decode_header
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ── CONFIGURACIÓN ──────────────────────────────────────
TELEGRAM_TOKEN = "8793854265:AAGcknvn_J7GZHm68txOnfAymSl0zKbg8DE"
GMAIL_USER     = "pedroluna157@gmail.com"
GMAIL_PASS     = "finrgkoighhgzzjd"
# ───────────────────────────────────────────────────────

def leer_emails(cantidad=5):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        _, mensajes = mail.search(None, "UNSEEN")
        ids = mensajes[0].split()[-cantidad:]
        resultado = []
        for uid in reversed(ids):
            _, data = mail.fetch(uid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            asunto = decode_header(msg["Subject"])[0][0]
            if isinstance(asunto, bytes):
                asunto = asunto.decode()
            remitente = msg["From"]
            resultado.append(f"📧 De: {remitente}\n📌 Asunto: {asunto}")
        mail.logout()
        return resultado if resultado else ["No hay emails nuevos."]
    except Exception as e:
        return [f"❌ Error: {e}"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Soy tu asistente.\n/emails — Ver emails no leídos")

async def ver_emails(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Revisando tu Gmail...")
    emails = leer_emails()
    for e in emails:
        await update.message.reply_text(e)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Recibí: {update.message.text}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("emails", ver_emails))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("✅ Bot corriendo...")
app.run_polling()