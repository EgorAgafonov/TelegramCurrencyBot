Telegram-бот для конвертации валют, распознавания текстов,
генерации QR-кодов и предоставления данных о юридических лицах РФ (ЕГРЮЛ).

Чат-бот, написанный в учебных целях, для ознакомления с библиотекой telebot для мессенджера Telegram.
Для обработки запросов об обменных курсах валют и предоставления сведений о юридических лицах РФ (ЕГРЮЛ), используются 
API-сервисы https://dadata.ru/api и https://www.exchangerate-api.com/ (необходима регистрация и получение TOKEN-ключей).
Запросы оптического распознавания текста (OCR) и генерации QR-кодов реализованы с помощью импортированных 
библиотек EasyOCR Reader и Segno.

Структура проекта представляет:
1) Корневую папку проекта с файлами main.py ("скелет" бота), utilities.py (классы с основными статическими 
методами и исключениями), settings (сведения о переменных среды, информация о доступных языках и валютах 
(используются стандарты ISO));
2) Папка chat_images для обработки и временного хранения изображений из бота;
3) Папка lxml_lessns содержит практические примеры использования методов различных библиотек и на прямую не используется
в данном проекте.

Агафонов Е.А., 2024 г.
