import json
import os
import shlex

from prettytable import PrettyTable  # pyright: ignore[reportMissingImports]

from .core import create_table, delete, drop_table, insert, select, update
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


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

def show_table(records, columns):
    table = PrettyTable()
    table.field_names = list(columns.keys())

    for record in records:
        row = []

        for column in columns:
            row.append(record.get(column))

        table.add_row(row)

    print(table)


def check_conditions(columns, condition):
    for name, value in condition.items():
        if name not in columns:
            print(f'Столбец {name} не существует')
            return False

        expected_type = columns[name]

        if expected_type == 'int':
            valid = type(value) is int
        elif expected_type == 'str':
            valid = type(value) is str
        elif expected_type == 'bool':
            valid = type(value) is bool
        else:
            valid = False

        if not valid:
            print(f'Неверный тип данных для столбца {name}')
            return False

    return True


def parse_value(value):
    value = value.strip()

    if value.startswith('"') and value.endswith('"'):
        result = json.loads(value)

        if type(result) is not str:
            raise ValueError('Неверная строка')

        return result

    if value.lower() == 'true':
        return True

    if value.lower() == 'false':
        return False

    try:
        return int(value)
    except ValueError:
        raise ValueError('Неверное значение')


def parse_condition(text):
    parts = text.split('=', 1)

    if len(parts) != 2:
        raise ValueError('Неверное условие')

    column = parts[0].strip()
    value = parse_value(parts[1])

    if not column:
        raise ValueError('Не указан столбец')

    return {column: value}


def parse_values(text):
    if not text.strip():
        return []

    parts = text.split(',')
    values = []

    for part in parts:
        values.append(parse_value(part))

    return values


def run():
    filepath = 'db_meta.json'

    while True:
            metadata = load_metadata(filepath)
            user_input = input('Введите данные: ').strip()

            if not user_input:
                continue

            arguments = shlex.split(user_input)

            if not arguments:
                continue

            command = arguments[0]

            if command == 'create_table':
                arguments = user_input.split()

                if len(arguments) < 3:
                    print('Недостаточно аргументов')
                    continue

                table_name = arguments[1]
                columns = arguments[2:]

                result = create_table(metadata, table_name, columns)

                if result is not None:
                    save_metadata(filepath, result)

            elif command == 'drop_table':
                if len(arguments) != 2:
                    print('Неверное количество аргументов')
                    continue

                table_name = arguments[1]

                if table_name not in metadata:
                    print('Таблица не существует')
                    continue

                result = drop_table(metadata, table_name)

                if result is not None:
                    save_metadata(filepath, result)

                    data_path = f'data/{table_name}.json'

                    if os.path.exists(data_path):
                        os.remove(data_path)

            elif command == 'list_tables':
                if len(arguments) != 1:
                    print('Неверное количество аргументов')
                    continue

                if metadata:
                    for table_name in metadata:
                        print(table_name)
                else:
                    print('Таблицы не найдены')

            elif command == 'insert':
                if not user_input.startswith('insert into '):
                    print('Неверная команда insert')
                    continue

                if ' values (' not in user_input:
                    print('Неверная команда insert')
                    continue

                if not user_input.endswith(')'):
                    print('Неверная команда insert')
                    continue

                parts = user_input.split(' values (', 1)

                table_name = parts[0].replace('insert into ', '').strip()
                values_text = parts[1][:-1]

                if not table_name or len(table_name.split()) != 1:
                    print('Неверное название таблицы')
                    continue

                values = parse_values(values_text)
                data = insert(metadata, table_name, values)

                if data is not None:
                    save_table_data(table_name, data)

            elif command == 'select':
                if not user_input.startswith('select from '):
                    print('Неверная команда select')
                    continue

                parts = user_input.split(' where ', 1)
                table_name = parts[0].replace('select from ', '').strip()

                if table_name not in metadata:
                    print('Таблица не существует')
                    continue

                columns = metadata[table_name]
                data = load_table_data(table_name)

                if len(parts) == 2:
                    condition = parse_condition(parts[1])

                    if not check_conditions(columns, condition):
                        continue

                    result = select(data, condition)
                else:
                    result = select(data)

                if result is not None:
                    show_table(result, columns)

            elif command == 'update':
                if ' set ' not in user_input or ' where ' not in user_input:
                    print('Неверная команда update')
                    continue

                parts = user_input.split(' set ', 1)
                table_name = parts[0].replace('update ', '').strip()

                if table_name not in metadata:
                    print('Таблица не существует')
                    continue

                conditions = parts[1].split(' where ', 1)
                set_clause = parse_condition(conditions[0])
                where_clause = parse_condition(conditions[1])

                columns = metadata[table_name]

                if not check_conditions(columns, set_clause):
                    continue

                if not check_conditions(columns, where_clause):
                    continue

                if 'ID' in set_clause:
                    print('Изменять ID нельзя')
                    continue

                data = load_table_data(table_name)
                found = select(data, where_clause)

                if not found:
                    print('Записи не найдены')
                    continue

                result = update(data, set_clause, where_clause)

                if result is not None:
                    save_table_data(table_name, result)
                    print('Записи успешно обновлены')

            elif command == 'delete':
                if not user_input.startswith('delete from '):
                    print('Неверная команда delete')
                    continue

                if ' where ' not in user_input:
                    print('Неверная команда delete')
                    continue

                parts = user_input.split(' where ', 1)
                table_name = parts[0].replace('delete from ', '').strip()

                if table_name not in metadata:
                    print('Таблица не существует')
                    continue

                columns = metadata[table_name]
                where_clause = parse_condition(parts[1])

                if not check_conditions(columns, where_clause):
                    continue

                data = load_table_data(table_name)
                found = select(data, where_clause)

                if not found:
                    print('Записи не найдены')
                    continue

                result = delete(data, where_clause)

                if result is not None:
                    save_table_data(table_name, result)
                    print('Записи успешно удалены')

            elif command == 'help':
                print_help()

            elif command == 'exit':
                print('Выход из программы')
                break

            else:
                print('Неизвестная команда')

        

            



    
