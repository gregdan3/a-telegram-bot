#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
from credentials import TOKEN
from noaa_sdk import noaa


def hello(bot, update):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def weather(bot, update, zipcode=35007, hourly=False):
    print("Ran weather function")
    weather_fetcher = noaa.NOAA()
    results = weather_fetcher.get_forecasts(zipcode, "US", hourly=hourly)
    print(results)
    for forecast in results:
        print(forecast)
        update.message.reply_text("%s" % forecast)
    # parse content
    # print it here


def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("hello", hello))
    updater.dispatcher.add_handler(CommandHandler("weather", weather))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
