import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print('Ошибка: Файл данных не найден')
        except KeyError as error:
            print(f'Ошибка: Таблица или столбец {error} не найден')
        except ValueError as error:
            print(f'Ошибка валидации: {error}')

        return None

    return wrapper

def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить {action_name}? [y/n]: '
            )

            if answer.lower() != 'y':
                print('Операция отменена')
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.monotonic()
            duration = end_time - start_time

            print(
                f'Функция {func.__name__} ' 
                f'выполнилась за {duration:,3f} секунд.'
                )

    return wrapper

def create_cacher():
    cache = {}

    def caсhe_result(key, value_func):
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result

        return result

    def clear_cache():
        cache.clear()

    return caсhe_result, clear_cache 