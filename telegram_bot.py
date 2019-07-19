#!/usr/bin/env python
import logging

import dateparser
from telegram.ext import Updater, CommandHandler
from noaa_sdk import noaa
from requests import get

from credentials import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def bot_help(bot, update):
    help_text = """
    Business Commands available:
    weather: Fetch the next 10 hours of weather from NOAA, by hour.
    dailyweather: Fetch the next 4 days of weather from NOAA, by half day.

    Fun Commands Available:
    tableflip: Flip a table.
    unflip: Put a table back.
    lenny: Random lenny face.
    shrug: Shrug at your foes.

    """
    update.message.reply_text(help_text)


def tableflip(bot, update):
    update.message.reply_text("(╯°□°）╯︵ ┻━┻")


def unflip(bot, update):
    update.message.reply_text(" ┬─┬ ノ( ゜-゜ノ)")


def shrug(bot, update):
    update.message.reply_text("¯\_(ツ)_/¯")


def lenny(bot, update):
    r = get("https://api.lenny.today/v1/random", verify=False).json()
    face = r[0]["face"]
    update.message.reply_text(face)


def weenie(bot, update):
    update.message.reply_test("You are, in fact, a weenie.")


def dailyweather(bot, update, zipcode="35007"):
    weather(bot, update, zipcode, hourly=False)


def hourlyweather(bot, update, zipcode="35007"):
    weather(bot, update, zipcode, hourly=True)


def weather(bot, update, zipcode="35007", hourly=True):
    weather_fetcher = noaa.NOAA()
    results = weather_fetcher.get_forecasts(zipcode, "US", hourly=hourly)
    if hourly:
        results = results[:10]  # 10 hours
        all_forecasts = parse_all_hourly_weather(results)
        update.message.reply_text(all_forecasts)
    else:
        results = results[1:6]  # each is a half day so 3 days
        all_forecasts = parse_all_daily_weather(results)
        update.message.reply_text(all_forecasts)


def parse_daily_weather(daily_forecast):
    time = daily_forecast["name"]
    # temperature = f"It will be {daily_forecast['temperature']} degrees {daily_forecast['temperatureUnit']}. "
    # wind_info = daily_forecast["windSpeed"]
    major_info = daily_forecast["detailedForecast"]
    return f"{time}: {major_info}."


def parse_all_daily_weather(daily_forecasts: list):
    forecasts = list()
    for forecast in daily_forecasts:
        result = parse_daily_weather(forecast)
        forecasts.append(result)
    return "\n".join(forecasts)


def parse_hourly_weather(hourly_forecast):
    time_start = dateparser.parse(hourly_forecast["startTime"])
    time_start = time_start.strftime("%I:%M %p")
    temperature = (
        f"{hourly_forecast['temperature']} {hourly_forecast['temperatureUnit']}"
    )
    major_info = hourly_forecast["shortForecast"]
    return f"{time_start}: {temperature}. {major_info}."


def parse_all_hourly_weather(hourly_forecasts: list):
    forecasts = list()
    for forecast in hourly_forecasts:
        result = parse_hourly_weather(forecast)
        forecasts.append(result)
    return "\n".join(forecasts)


def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("weather", hourlyweather))
    updater.dispatcher.add_handler(CommandHandler("dailyweather", dailyweather))

    updater.dispatcher.add_handler(CommandHandler("tableflip", tableflip))
    updater.dispatcher.add_handler(CommandHandler("unflip", unflip))
    updater.dispatcher.add_handler(CommandHandler("shrug", shrug))

    updater.dispatcher.add_handler(CommandHandler("lenny", lenny))

    updater.dispatcher.add_handler(CommandHandler("weenie", weenie))

    updater.dispatcher.add_handler(CommandHandler("help", bot_help))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
