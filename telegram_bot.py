#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler
from credentials import TOKEN
from noaa_sdk import noaa


def hello(bot, update):
    update.message.reply_text("Hello {}".format(update.message.from_user.first_name))


def weather(bot, update, zipcode=35007, hourly=False):
    print("Ran weather function")
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

    updater.dispatcher.add_handler(CommandHandler("hello", hello))
    updater.dispatcher.add_handler(CommandHandler("weather", weather))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
