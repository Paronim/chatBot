import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
import string
# from sklearn.feature_extraction.text import TfidVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.svm import LinearSVC

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я кот программиста, не хочешь пообщаться?")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не знаю таких слов, даже в языках прогаммирования")


# def remove_punctuation(text):
#     translator = str.maketrans('', '', string.punctuation)
#     return text.translate(translator)

# vectorizer = TfidVectorizer(analyzer=’char_wb’, ngram_range=(2,3), max_df=0.8)
# vector = vectorizer.fit_transform(text)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, stratify=y)

# clf = LinearSVC()
# clf.fit(X_train, y_train)
# clf.predict(vector)[0]

if __name__ == '__main__':
    application = ApplicationBuilder().token(
        '6445005733:AAHEsYlizkEoHDyCc_qnHG4bMBcSgfd3aMw').build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
