# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

user = os.getenv("USER")  # Пользователь для прокси
password = os.getenv("PASSWORD")  # Пароль для прокси
port = os.getenv("PORT")  # Порт для прокси
ip = os.getenv("IP")  # IP адрес прокси

def setup_proxy():
    # Проверяем, что все необходимые переменные окружения установлены
    if user and password and ip and port:
        # Указываем прокси для HTTP и HTTPS
        os.environ['http_proxy'] = f"http://{user}:{password}@{ip}:{port}"
        os.environ['https_proxy'] = f"http://{user}:{password}@{ip}:{port}"
    else:
        # Если переменные окружения не установлены, пропускаем настройку прокси
        print("[!] Переменные окружения для прокси не установлены. Продолжаем без прокси.")