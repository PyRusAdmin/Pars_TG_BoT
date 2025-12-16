# -*- coding: utf-8 -*-
import asyncio
import json
import os
from datetime import datetime

import mistune  # Библиотека для работы с Markdowns
from loguru import logger
from rich import print
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, MessageMediaDocument, MessageMediaPhoto

from system.config_class import ConfigClass
from system.system_setting import connecting_new_account, checking_accounts
from system.system_setting import console

# Логирование программы
logger.add("setting/log/log.log", rotation="1 MB", compression="zip")
config_manager = ConfigClass()


def find_file_in_folder(folder_path, file_extension):
    """
    Функция принимает путь к папке и расширение файла.
    Возвращает имя файла с заданным расширением, найденного в папке.
    Если такого файла нет, возвращает None.
    :param folder_path: Путь к папке
    :param file_extension: расширение файла
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_extension):
            return file_name
    return None


async def connecting_to_an_account(api_id: int, api_hash: str):
    """
    Устанавливает соединение с учетной записью Telegram.
    :param api_id: id аккаунта Telegram
    :param api_hash: хэш аккаунта Telegram
    """
    file_name = find_file_in_folder(folder_path='accounts', file_extension='.session')
    if file_name:
        print(f'Найден аккаунт {file_name}')
        # Устанавливаем соединение с аккаунтом Telegram
        client = TelegramClient(f'accounts/{file_name}', api_id, api_hash, system_version="4.16.30-vxCUSTOM")
        await client.connect()
        return client
    else:
        print('Аккаунт не найден')


async def download_images_from_telegram_channel(channel_url: str, ) -> None:
    """
    Функция скачивает все изображения из заданного канала Telegram
    :param channel_url: ссылка на канал Telegram, например "https://t.me/+VrDS1_bG0bExNzQy"
    """
    # Чтение API ID и API Hash
    api_id, api_hash = config_manager.reading_the_id_and_hash()
    client = await connecting_to_an_account(api_id, api_hash)
    channel = await client.get_entity(channel_url)  # Получаем объект канала
    peer_channel = PeerChannel(channel.id)  # Получаем ID чата или группы

    async for message in client.iter_messages(peer_channel):  # Перебираем посты
        # Если в посте есть медиафайлы
        if message.media is not None:
            print(f"Downloading media from post {message.id}")
            # Определяем дату и время публикации поста
            post_date = datetime.fromtimestamp(message.date.timestamp()).strftime('%Y-%m-%d_%H-%M_%S')
            # Создаем папку с датой и временем поста, если ее еще нет
            folder_path = f"download/{post_date}"
            os.makedirs(folder_path, exist_ok=True)

            logger.info(f"Info: {message}")
            logger.info(f"Info: {message.message}")  # Просмотр текста описания поста

            if message.message == "":  # Если нет текста описания поста, то не заносим в файл json
                pass
            else:

                markdown_renderer = mistune.create_markdown()  # Создаем рендерер Markdown
                markdown_text = markdown_renderer(message.message)  # Преобразуем текст в Markdown

                with open(f"{folder_path}/{message.id}.json", 'w', encoding='utf-8') as json_file:
                    json.dump(markdown_text, json_file, ensure_ascii=False, indent=4)

            # Обработка видео
            if isinstance(message.media, MessageMediaDocument):
                # Имя файла включает идентификатор поста и идентификатор фотографии
                file_path = f"{folder_path}/{message.id}.mp4"
                # Скачиваем медиафайл
                await message.download_media(file_path)
                print(f"Downloaded media to {file_path}")

                # Извлекаем file_id видео
                file_id = message.media.document.id
                # Создаём словарь с информацией о file_id
                file_id_data = {
                    "message_id": message.id,
                    "file_id": str(file_id),  # Преобразуем в строку для JSON
                    "file_path": file_path,
                    "date": post_date
                }
                # Сохраняем file_id в отдельный JSON-файл
                with open(f"{folder_path}/{message.id}_file_id.json", 'w', encoding='utf-8') as file_id_file:
                    json.dump(file_id_data, file_id_file, ensure_ascii=False, indent=4)
                print(f"Saved file_id to {folder_path}/{message.id}_file_id.json")

            # Обработка фото
            elif isinstance(message.media, MessageMediaPhoto):
                # Имя файла включает идентификатор поста и идентификатор фотографии
                file_path = f"{folder_path}/{message.id}.jpg"
                # Скачиваем медиафайл
                await message.download_media(file_path)
                print(f"Downloaded media to {file_path}")

    await client.disconnect()  # Закрываем соединение


async def main():
    """Основное окно программы"""
    await checking_accounts()
    try:
        print("[bold red]\n"
              "Дата создания: 28.04.2023\n"
              "Версия программы: 0.0.6\n"
              "[bold green][1] - Подключение нового аккаунта\n"
              "[bold green][2] - Запуск parsing\n"
              "[bold green][3] - Настройки\n")
        user_input = console.input("[bold red][+] Введите номер : ")  # Вводим номер
        if user_input == "1":  # Подключение нового аккаунта
            await connecting_new_account()
        elif user_input == "2":  # Запуск parsing
            channel_url = config_manager.reading_the_link_to_the_group()
            await download_images_from_telegram_channel(channel_url)
        elif user_input == "3":  # Настройки
            print("[bold green][1] - Запись api_id и api_hash\n"
                  "[bold green][2] - Запись ссылки, для дальнейшего parsing\n")
            user_input = console.input("[bold red][+] Введите номер : ")  # Вводим номер
            if user_input == "1":  # Запись api_id и api_hash
                print("[bold red][!] Получить api_id, api_hash можно на сайте https://my.telegram.org/auth")
                # Запись API ID и API Hash
                await config_manager.writing_api_id_api_hash()
                await main()  # После не правильного ввода номера возвращаемся в начальное меню
            elif user_input == "2":  # Запись ссылки, для дальнейшего parsing
                print(f"[bold green][!] Давайте запишем ссылку для parsing, ссылка должна быть [bold red]одна!")
                # Запись ссылки на группу
                await config_manager.writing_link_to_the_group()
                await main()  # После не правильного ввода номера возвращаемся в начальное меню
            else:
                await main()  # После не правильного ввода номера возвращаемся в начальное меню
        else:
            await main()  # После не правильного ввода номера возвращаемся в начальное меню
    except KeyboardInterrupt:  # Закрытие окна программы
        print("[!] Скрипт остановлен!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
        print("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
