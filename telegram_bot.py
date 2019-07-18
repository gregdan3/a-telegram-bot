#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
from credentials import TOKEN


def hello(bot, update):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("hello", hello))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
