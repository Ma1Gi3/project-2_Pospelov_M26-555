from .utils import load_table_data


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}

    for column in columns:
        if column.count(":") != 1:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        name, data_type = column.split(":")

        if not name or data_type not in ("int", "str", "bool"):
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        if name in table_columns:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        table_columns[name] = data_type

    metadata[table_name] = table_columns

    result = []

    for name, data_type in table_columns.items():
        result.append(f"{name}:{data_type}")

    print(f'Таблица "{table_name}" успешно создана со столбцами:')
    print(", ".join(result))

    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata

def insert(metadata, table_name, values):
    if table_name not in metadata:
        print('Таблица не существует')
        return None

    columns = metadata[table_name]

    column_names = []

    for name in columns:
        if name != 'ID':
            column_names.append(name)

    if len(values) != len(column_names):
        print('Неверное количество значений')
        return None

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
            print(f'Неверный тип данных для столбца {name}')
            return None

    data = load_table_data(table_name)

    new_id = 1

    for record in data:
        if record['ID'] >= new_id:
            new_id = record['ID'] + 1

    new_record = {'ID': new_id}

    for i in range(len(values)):
        new_record[column_names[i]] = values[i]

    data.append(new_record)

    print(f'Запись успешно добавлена. ID = {new_id}')

    return data

def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    result = []

    for record in table_data:
        matches = True

        for name, value in where_clause.items():
            if record.get(name) != value:
                matches = False

        if matches:
            result.append(record)

    return result

def update(table_data, set_clause, where_clause):
    for record in table_data:
        matches = True

        for name, value in where_clause.items():
            if record.get(name) != value:
                matches = False

        if matches:
            for name, value in set_clause.items():
                record[name] = value

    return table_data

def delete(table_data, where_clause):
    result = []

    for record in table_data:
        matches = True

        for name, value in where_clause.items():
            if record.get(name) != value:
                matches = False

        if not matches:
            result.append(record)

    return result


   







    




    