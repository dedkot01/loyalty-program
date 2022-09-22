# Loyalty Program

## Запуск

Вызов команды в терминале:
```
python loyalty_program/app.py
```

## Конфигурация

Для работы веб-приложения необходимо в директорию `loyalty_program` добавить файл конфигурации `config.py`:
```
conn_string = 'text'         # строка подключения к СУБД
secret_key = b'very_secret'  # 

#  стартовый пользователь, создаётся при первом запуске веб-приложения
admin_login = 'login'        # логин для админа системы
admin_password = 'password'  # пароль для админа системы
```
