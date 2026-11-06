permissible_types = ("int", "str", "bool")

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}
    
    for column in columns:
        try:
            name, type_ = column.split(':')
        except ValueError:
            print('Некорректный тип данных')
            return metadata
    if type_ not in permissible_types:
        print('Некорретный тип данных')
        return metadata

    if name in table_columns:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
    
    metadata[table_name] = table_columns

    correct_columns = []

    for name, data_type in table_columns.items():
        correct_columns.append(f"{name}:{data_type}")

    print(f'Таблица "{table_name}" успешно создана:')
    print(", ".join(correct_columns))

    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata








    




    