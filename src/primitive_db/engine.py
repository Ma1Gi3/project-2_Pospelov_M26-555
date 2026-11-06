import shlex
from .core import create_table, drop_table
from .utils import load_metadata, save_metadata

# src/primitive_db/engine.py
def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 

def run():
    filepath = 'db_meta.json'
    
    while True:
        metadata = load_metadata(filepath)

        user_input = input('Введите данные: ')

        try:
            arguments = shlex.split(user_input)
        except ValueError:
            print('Неверная команда')
            continue

        if not arguments:
            continue

        comands = arguments[0]

        if comands == 'create_table':
            if len(arguments) < 3:
                print('Недостаточно аргументов для создания таблицы')
                continue

            table_name = arguments[1]
            columns = arguments[2:]

            metadata = create_table(metadata, table_name, columns)
            save_metadata(filepath, metadata)

        elif comands == 'drop_table':
            if len(arguments) != 2:
                print('Неверное количество аргументов')
                continue

            table_name = arguments[1]

            metadata = drop_table(metadata, table_name)
            save_metadata(filepath, metadata)

        elif comands == 'list_table':
            if len(arguments) != 1:
                print('Неверное количество аргументов')
                continue

            if metadata:
                for table_name in metadata:
                    print(f'{table_name}')
            else:
                print('Таблицы не найдены')

        elif comands == 'help':
            if len(arguments) != 1:
                print('Неверное количество аргументоа')
                continue

            print_help()

        elif comands == 'exit':
            if len(arguments) != 1:
                print('Неверное количество аргументов')
                continue

        print('Выход из программы')
        break

    else:
        print(f'Функции {comands} не найдено, повторите попытку')
            



    
