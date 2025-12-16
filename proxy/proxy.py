# -*- coding: utf-8 -*-
import os


def setup_proxy(user, password, ip, port):
    # Указываем прокси для HTTP и HTTPS
    os.environ['http_proxy'] = f"http://{user}:{password}@{ip}:{port}"
    os.environ['https_proxy'] = f"http://{user}:{password}@{ip}:{port}"