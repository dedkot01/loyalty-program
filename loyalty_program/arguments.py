import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Сервер веб-приложения программы лояльности заведения "Крылья"',
    )

    parser.add_argument(
        '--host', type=str,
        help='адрес хоста, по которому будет доступен сервер (127.0.0.1 - локальная сеть, 0.0.0.0 - глобальная сеть)',
    )

    parser.add_argument(
        '--port', type=int,
        help='порт, по которому будет доступен сервер',
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='включить режим отладки сервера',
    )

    return parser.parse_args()
