import configparser

from rich.console import Console


class ConfigClass:
    def __init__(self, config_file_path='setting/config.ini'):
        """
        Инициализация класса для работы с конфигурационным файлом.
        :param config_file_path: Путь к конфигурационному файлу.
        """
        self.config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
        self.config_file_path = config_file_path
        self.console = Console()
        # Чтение конфигурационного файла
        self.config.read(self.config_file_path)

    async def writing_link_to_the_group(self) -> configparser.ConfigParser:
        """
        Записываем ссылку для парсинга групп/каналов.
        :return: Обновленный объект ConfigParser.
        """
        target_group_entity_user = self.console.input(
            "[bold green][+] Введите ссылку на группу: ")  # Вводим ссылку на группу

        # Проверяем, существует ли секция 'link_to_the_group'
        if 'link_to_the_group' not in self.config:
            self.config['link_to_the_group'] = {}

        # Обновляем значение в конфигурации
        self.config.set('link_to_the_group', 'target_group_entity', target_group_entity_user)

        # Записываем изменения в файл
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)

        return self.config

    async def writing_api_id_api_hash(self) -> configparser.ConfigParser:
        """
        Записываем api_id и api_hash, полученные с помощью регистрации приложения на сайте https://my.telegram.org/auth.
        :return: Обновленный объект ConfigParser.
        """
        api_id_data = self.console.input("[bold green][+] Введите api_id: ")
        api_hash_data = self.console.input("[bold green][+] Введите api_hash: ")

        # Обновляем значения в конфигурации
        if 'telegram_settings' not in self.config:
            self.config['telegram_settings'] = {}
        self.config.set('telegram_settings', 'id', api_id_data)
        self.config.set('telegram_settings', 'hash', api_hash_data)

        return self.config

    def reading_the_link_to_the_group(self):
        """
        Считываем ссылку для парсинга групп/каналов из конфигурационного файла.
        :return: Ссылка для парсинга групп/каналов.
        """
        # Убедимся, что файл прочитан
        self.config.read(self.config_file_path)
        # Получаем значения из конфигурации
        channel_url = self.config.get('link_to_the_group', 'target_group_entity', fallback=None)

        return channel_url

    def reading_the_id_and_hash(self):
        """
        Считываем api_id и api_hash из конфигурационного файла.
        :return: Кортеж (api_id, api_hash).
        """
        # Убедимся, что файл прочитан
        self.config.read(self.config_file_path)

        # Получаем значения из конфигурации
        api_id_data = self.config.get('telegram_settings', 'id', fallback=None)
        api_hash_data = self.config.get('telegram_settings', 'hash', fallback=None)

        if not api_id_data or not api_hash_data:
            raise ValueError("API ID или API Hash не найдены в конфигурационном файле.")

        return api_id_data, api_hash_data

    def writing_settings_to_a_file(self):
        """
        Запись данных в файл конфигурации.
        """
        with open(self.config_file_path, 'w') as config_file:
            self.config.write(config_file)
