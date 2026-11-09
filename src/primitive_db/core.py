from .decorators import confirm_action, create_cacher, handle_db_errors, log_time
from .utils import load_table_data

PERMISSIBLE_TYPES = ['int', 'str', 'bool']

cache_result, clear_cache = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу"""
    if table_name in metadata:
        print('Таблица уже существует')
        return None

    if not table_name.isidentifier():
        raise ValueError('Некорректное название таблицы')

    table_columns = {'ID': 'int'}

    for column in columns:
        parts = column.split(':')

        if len(parts) != 2:
            raise ValueError('Неверный формат столбца')

        name, type_ = parts

        if type_ not in PERMISSIBLE_TYPES:
            raise ValueError('Некорректный тип данных')

        if not name.isidentifier() or name in table_columns:
            raise ValueError(f'Некорректное название столбца: {name}')

        table_columns[name] = type_

    metadata[table_name] = table_columns

    print(f'Таблица "{table_name}" успешно создана')

    return metadata


@handle_db_errors
@confirm_action('удаление таблицы')
def drop_table(metadata, table_name):
    """Удаляет таблицу из базы данных"""
    if table_name not in metadata:
        raise KeyError(table_name)

    del metadata[table_name]

    clear_cache()

    print(f'Таблица "{table_name}" удалена')

    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу"""
    if table_name not in metadata:
        raise KeyError(table_name)

    columns = metadata[table_name]

    column_names = []

    for name in columns:
        if name != 'ID':
            column_names.append(name)

    if len(values) != len(column_names):
        raise ValueError('Неверное количество значений')

    for i in range(len(values)):
        name = column_names[i]
        expected_type = columns[name]
        value = values[i]

        if expected_type == 'int':
            valid = type(value) is int
        elif expected_type == 'str':
            valid = type(value) is str
        elif expected_type == 'bool':
            valid = type(value) is bool
        else:
            valid = False

        if not valid:
            raise ValueError(f'Неверный тип данных: {name}')

    data = load_table_data(table_name)

    new_id = 1

    for record in data:
        if record['ID'] >= new_id:
            new_id = record['ID'] + 1

    new_record = {'ID': new_id}

    for i in range(len(values)):
        new_record[column_names[i]] = values[i]

    data.append(new_record)

    clear_cache()

    print(f'Запись добавлена. ID = {new_id}')

    return data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или записи подходящие под условие"""
    key = (repr(table_data), repr(where_clause))

    def get_result():
        result = []

        for record in table_data:
            matches = True

            if where_clause is not None:
                for name, value in where_clause.items():
                    if record.get(name) != value:
                        matches = False

            if matches:
                result.append(record.copy())

        return result

    return cache_result(key, get_result)


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Изменяет записи, подходящие под условие"""
    for record in table_data:
        matches = True

        for name, value in where_clause.items():
            if record.get(name) != value:
                matches = False

        if matches:
            for name, value in set_clause.items():
                record[name] = value

    clear_cache()

    return table_data


@handle_db_errors
@confirm_action('удаление записей')
def delete(table_data, where_clause):
    """Удаляет записи, подходящие под условие"""
    result = []

    for record in table_data:
        matches = True

        for name, value in where_clause.items():
            if record.get(name) != value:
                matches = False

        if not matches:
            result.append(record)

    clear_cache()

    return result


   







    




    