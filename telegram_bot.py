#!/usr/bin/env python
import logging
from functools import partial

from requests import get
from telegram.error import TelegramError
from telegram.ext import CommandHandler, Updater

from credentials import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

MEALPAGE = r"https://www.themealdb.com/api/json/v1/1/random.php"
LENNYPAGE = r"https://api.lenny.today/v1/random"
WTTRPAGE = r"https://wttr.in/?format=%c+%l:+%C+%t+%w+%h"
TABLEFLIP = r"(╯°□°）╯︵ ┻━┻"
UNFLIP = r" ┬─┬ ノ( ゜-゜ノ)"
SHRUG = r"¯\_(ツ)_/¯"


def reply(update, context, text):
    """to be used with partial, but that only passes leftmost *args"""
    update.message.reply_text(text)


def long_parse_meal(mealjson):
    mealjson = mealjson["meals"][0]  # unwrap
    name = mealjson["strMeal"]
    kind = mealjson["strCategory"]
    origin = mealjson["strArea"]
    instructions = mealjson["strInstructions"]
    image = mealjson["strMealThumb"]

    # this is the worst thing i've ever written
    ingredients = ", ".join(
        [
            f"{mealjson[f'strMeasure{i}']} {mealjson[f'strIngredient{i}']}".strip()
            for i in range(1, 21)
            if mealjson[f"strIngredient{i}"]
        ]
    )
    return f"{name}\n\nA(n) {origin} meal, {kind}\n{instructions}\n\n{ingredients}\n\n{image}"


def meal(update, context, long=False):
    r = get(MEALPAGE).json()
    if long:
        mealtext = long_parse_meal(r)
    else:
        mealtext = f"You should have {r['meals'][0]['strMeal']} to eat!"
    update.message.reply_text(mealtext)


def lenny(update, context):
    r = get(LENNYPAGE).json()[0]["face"]
    update.message.reply_text(r)


def error(update, context, error):
    # TODO
    update.message.reply_text(error.__str__)


def weather(update, context):
    r = get(WTTRPAGE).text
    update.message.reply_text(r)


def main():
    # help is a special case of the constants
    HELP = ""

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler("tableflip", partial(reply, text=TABLEFLIP))
    )
    HELP += "tableflip: Flip a table\n"

    updater.dispatcher.add_handler(
        CommandHandler("unflip", partial(reply, text=UNFLIP))
    )
    HELP += "unflip: Put a table back\n"

    updater.dispatcher.add_handler(CommandHandler("shrug", partial(reply, text=SHRUG)))
    HELP += "shrug: Shrug at your foes\n"

    updater.dispatcher.add_handler(CommandHandler("lenny", lenny))
    HELP += "lenny: Random lenny face\n"

    HELP += "\n"

    updater.dispatcher.add_handler(CommandHandler("weather", weather))
    HELP += "weather: Fetch the current weather from wttr.in\n"

    updater.dispatcher.add_handler(CommandHandler("meal", meal))
    HELP += "meal: Get a randomly selected meal\n"

    updater.dispatcher.add_handler(CommandHandler("longmeal", partial(meal, long=True)))
    HELP += "longmeal: Get a randomly selected meal with instructions and ingredients\n"

    updater.dispatcher.add_handler(CommandHandler("help", partial(reply, text=HELP)))
    HELP += "help: Send this message!"

    # TODO: error handler

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
