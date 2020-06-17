import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
import requests
import sqlite3

import parser

print("bot start...")
@bot.message_handler(commands=['start'])
def start(message):
    pass


@bot.message_handler(content_types=['text'])
def body(message):
    pass


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Что-то пошло не так."
                                                " Повторите попытку позже.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Вы успешно сделали транзакцию на `{} {}`! '.format(message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    pass
