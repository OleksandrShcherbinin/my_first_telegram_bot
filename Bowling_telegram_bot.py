from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, \
    InlineQueryResultArticle, ParseMode
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, InlineQueryHandler
import logging

updater = Updater(token='Add your telegram token here')

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привіт! Я Боулінг Бот')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('bowling_logo_small.jpg', 'rb'))
    bot.send_message(chat_id=update.message.chat_id,
                     text='Готовий з радістю Вам допомогти!')
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                          text=main_menu_message(), reply_markup=main_menu_keyboard())


def first_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=first_menu_message(),
                          reply_markup=first_menu_keyboard())


def second_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=second_menu_message(),
                          reply_markup=second_menu_keyboard())


def third_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=third_menu_message(),
                          reply_markup=third_menu_keyboard())


def first_submenu(bot, update):
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    pass


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    answer = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(answer)


def second_submenu(bot, update):
    pass


def third_submenu(bot, update):
    pass


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Забронювати доріжку(столик)', callback_data='m1')],
                [InlineKeyboardButton('Дізнатися ціни', callback_data='m2')],
                [InlineKeyboardButton('Замовити дзвінок', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Боулінг у Соснівці', callback_data='m1_1')],
                [InlineKeyboardButton('Боулінг на Митниці(Дніпроплаза)', callback_data='m1_2')],
                [InlineKeyboardButton('До головного меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Боулінг', callback_data='m2_1',
                                      url='http://cosmos-bowling.com/upload/images/____________1_6_%281%29.jpg')],
                [InlineKeyboardButton('Більярд', callback_data='m2_2',
                                      url='http://cosmos-bowling.com/upload/images/____________2_6_%281%29.jpg')],
                [InlineKeyboardButton('Бар', callback_data='m2_3',
                                      url='http://cosmos-bowling.com/category/17/nashe-menyu-bar/')],
                [InlineKeyboardButton('Ресторан', callback_data='m2_4',
                                      url='http://cosmos-bowling.com/category/18/menyu/')],
                [InlineKeyboardButton('До головного меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def third_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Боулінг у Соснівці', callback_data='m3_1')],
                [InlineKeyboardButton('Боулінг на Митниці', callback_data='m3_2')],
                [InlineKeyboardButton('До головного меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def main_menu_message():
    return 'Оберіть, що саме Вас цікавить:'


def first_menu_message():
    return 'В якому клубі забронувати доріжку:'


def second_menu_message():
    return 'Дізнатися ціну на:'


def third_menu_message():
    return 'Дзвінок'


start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))

updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))

dispatcher.add_handler(start_handler)
updater.start_polling()
updater.idle()


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text + ' Я Космос Боулинг Бот!')


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)
