#!/usr/bin/env python3

from os import listdir
from json import loads, dump

# from aiogram import types

from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from config import *
import keyboards.client_kb as keyboard
import admin


def history_record(req, file='json/history.json'):
    with open(file, 'a') as f:
        dump(req, f, indent=4, ensure_ascii=False)
        f.write('\n')
    return True


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_message_text = '''🍀<b>Вас приветствует GreenWayShop</b>🍀
    
Мы с заботой относимся к защите окружающей среды, 
поэтому каждый наш продукт разработан 
по принципу безопасности и экологичности

Здесь вы можете найти всё что вам нужно для:

🏡 <b>Дома</b>
🚗 <b>Машины</b>
✨ <b>Ухода за собой</b>
🐶 <b>Ваших любимых питомцев</b>.

У нас присутствует <b>бонусная система</b> Приводите друзей - 
получайте подарки,
 и предложения специально для вас😊'''
    await bot.send_message(message.from_user.id,
                           f'Здравствуйте, {message.from_user.first_name}',
                           reply_markup=keyboard.menu_kb(message)['kb'])
    await bot.send_message(message.from_user.id, start_message_text,
                           reply_markup=keyboard.menu_kb(message)['callback'])


@dp.message_handler(content_types=['text'])
async def message_handler(message: types.Message):
    message_text = message.text

    if '🛍' in message_text:
        await bot.send_message(message.from_user.id,
                               '🛍', reply_markup=keyboard.catalog()['kb'])
        await bot.send_message(message.from_user.id,
                               'Выберите раздел:',
                               reply_markup=keyboard.catalog()['callback'])
    elif '📃' in message_text:
        await bot.send_message(message.from_user.id,
                               '📃 История заказов',
                               reply_markup=keyboard.menu_kb(message))
    elif '🛒' in message_text:
        await bot.send_message(message.from_user.id,
                               '🛒', reply_markup=keyboard.menu_kb(message))
    elif '📅' in message_text:
        await bot.send_message(message.from_user.id, '📅 Новости',
                               reply_markup=keyboard.menu_kb(message))
    elif '⚙' in message_text:
        await bot.send_message(message.from_user.id, '⚙ Настройки',
                               reply_markup=keyboard.menu_kb(message))
    elif '⭐' in message_text:
        await bot.send_message(message.from_user.id, '⭐ Избранное',
                               reply_markup=keyboard.menu_kb(message))
    elif '🏡' in message_text:
        await bot.send_message(message.from_user.id, '🏡',
                               reply_markup=keyboard.menu_kb(message)['kb'])
    elif '🔑' in message.text:
        if admin.admin_check(message):
            await bot.send_message(message.chat.id,
                                'Добро пожаловать в Админ-панель',
                                reply_markup=keyboard.admin_kb())
        else:
            await bot.send_message(message.chat.id,
                                   'Такого товара не существует')


@dp.callback_query_handler(text='popular')
async def popular(callback: types.CallbackQuery):
    await callback.answer('Popular')


@dp.callback_query_handler(text='textile')
async def textile(callback: types.CallbackQuery):
    work_dir = './json/data/textile/'
    subsections_names = listdir(work_dir)  # get filenames in a dir
    await callback.message.edit_text(text='Выберите раздел:',
                                     reply_markup=keyboard.subsections_cb(
                                         'textile_sb_',
                                         subsections_names))


@dp.callback_query_handler(Text(startswith='textile_sb_'))
async def textile_subsections(callback: types.CallbackQuery):
    work_dir = './json/data/textile/'
    file = None

    if 'Для Авто' in callback.data:
        file = 'Для Авто'
    elif 'Для Тела' in callback.data:
        file = 'Для Тела'
    elif 'Для Уборки' in callback.data:
        file = 'Для Уборки'

    with open(work_dir + file + '.json') as f:
        json = loads(f.read())
    for i in range(len(json)-1):
        print(i)
        message_markup = dict(
            image=f'{json[i]["image"]}',
            name=f'<b>{json[i]["name"]}</b>',
            price=f'Цена:  {int(json[i]["price"])}'
        )
        message = f'''
         {message_markup['image']}
        {message_markup['name']}\n
        {message_markup['price']}
                    '''

        await bot.send_message(callback.from_user.id, message)
        await callback.answer()


@dp.callback_query_handler(text='house')
async def house(callback: types.CallbackQuery):
    work_dir = './json/data/house/'
    subsections_names = listdir(work_dir)  # get filenames in a dir
    await callback.message.edit_text(text='Выберите раздел:',
                                     reply_markup=keyboard.subsections_cb(
                                         'house_sb_',
                                         subsections_names))


@dp.callback_query_handler(Text(startswith='house_sb_'))
async def textile_subsections(callback: types.CallbackQuery):
    work_dir = './json/data/house/'
    file = None
    if 'Средства для стирки' in callback.data:
        file = 'Средства для стирки'
    elif 'Средства для уборки' in callback.data:
        file = 'Средства для уборки'
    elif 'Швабры' in callback.data:
        file = 'Швабры'
    try:
        with open(work_dir + file + '.json') as f:
            json = loads(f.read())
        for i in range(len(json)):
            message_markup = dict(
                image=f'{json[i]["image"]}',
                name=f'<b>{json[i]["name"]}</b>',
                price=f'Цена: {int(json[i]["price"])}'
            )
            print(message_markup['name'])
            message = f'''
            {message_markup['image']}
            {message_markup['name']}\n
            {message_markup['price']}
                        '''
            await bot.send_message(callback.from_user.id, message)
            await callback.answer()
    except TypeError:
        await bot.send_message(callback.from_user.id,
                               'Приносим свои извенения, '
                               'что-то пошло не так 😰 \n'
                               'Попробуйте пожалуйста ещё раз')
        await callback.answer()

if __name__ == '__main__':
    executor.start_polling(dp)
