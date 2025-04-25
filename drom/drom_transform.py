import pandas as pd


def transform_drom_data():
    """Преобразует и очищает данные об автомобилях из файла json.

    Функция выполняет следующие преобразования:
    - Извлекает марку, модель и год из названия автомобиля
    - Преобразует цену в числовой формат
    - Разбирает характеристики двигателя на отдельные компоненты
    - Нормализует типы кузова, привода и коробки передач
    - Преобразует дату публикации в формат datetime
    - Удаляет некорректные записи
    - Приводит все строковые значения к нижнему регистру
    - Преобразует пробег в числовой формат
    - Удаляет ненужные столбцы

    Args:
        Нет параметров (работает с файлом json)

    Returns:
        pandas.DataFrame: Очищенный DataFrame с автомобилями, содержащий столбцы:
            - brand (str): Марка автомобиля
            - model (str): Модель автомобиля
            - year (int): Год выпуска
            - price (int): Цена в рублях
            - engine_volume (float): Объем двигателя
            - engine_type (str): Тип двигателя
            - body_type (str): Тип кузова
            - drive_type (str): Тип привода
            - transmission (str): Тип коробки передач
            - mileage (int): Пробег в км
            - location (str): Местоположение
            - publication_date (datetime): Дата публикации
            - description (str): Описание
            - link (str): Ссылка на объявление

    Raises:
        FileNotFoundError: Если файл autoru_data.json не найден
        JSONDecodeError: Если файл содержит некорректный JSON
        KeyError: Если в данных отсутствуют ожидаемые столбцы

    Examples:
        >>> df = transform_drom_data()
        >>> print(df.columns)
        Index(['brand', 'model', 'year', 'price', 'engine_volume', 'engine_type',
               'body_type', 'drive_type', 'transmission', 'mileage', 'location',
               'publication_date', 'description', 'link'],
              dtype='object')
    """
    def extract_car_info(title):
        parts = title.split(' ')
        brand = parts[1]
        model_parts = parts[2]
        model = "".join(part for part in model_parts if ',' not in part)
        year_part = title.split(',')[1].strip()
        year = "".join(filter(str.isdigit, year_part))[:4]
        return brand, model, int(year)

    def extract_engine(engine):
        parts = engine.replace(" ", "").split(',')
        engine_type = parts[0]
        engine_volume = parts[1][:-1]
        return engine_type, float(engine_volume)

    def transform_transmission(transmission):
        if transmission == "механика":
            return "механическая"
        return "автоматическая"

    def extract_mileage(mileage):
        parts = mileage.replace(" ", "").split(',')
        mileage = parts[0][:-2]
        return int(mileage)

    def extract_drive_type(drive_type):
        if drive_type not in ['4WD', 'передний', 'задний']: return None
        if drive_type == "4WD":
            return "полный"
        return drive_type

    def extract_location(location):
        if location == "Не указано": return None
        return 'москва'

    def extract_publication(publication):
        publication_date = publication.split("от")[1].strip()
        return publication_date

    drom_df = pd.read_json('drom_data.json')

    drom_df['title'] = drom_df['title'].replace("Не указано", None)
    drom_df.dropna(subset=['title'], inplace=True)
    drom_df[['brand', 'model', 'year']] = drom_df['title'].apply(extract_car_info).apply(pd.Series)
    drom_df['price'] = drom_df['price'].apply(lambda x: x.replace(' ', '')[:-1]).astype(int)
    drom_df[['engine_type', 'engine_volume']] = drom_df['engine'].apply(extract_engine).apply(pd.Series)
    drom_df['transmission'] = drom_df['transmission'].apply(transform_transmission).apply(pd.Series)
    drom_df['mileage'] = drom_df['mileage'].apply(extract_mileage).apply(pd.Series)
    drom_df['power'] = drom_df['power'].astype(int)
    drom_df['drive_type'] = drom_df['drive_type'].apply(extract_drive_type).apply(pd.Series)
    drom_df['location'] = drom_df['location'].apply(extract_location).apply(pd.Series)
    drom_df['publication_date'] = drom_df['publication_date'].apply(extract_publication).apply(pd.Series)
    drom_df['publication_date'] = pd.to_datetime(drom_df['publication_date'], format='%d.%m.%Y')
    drom_df = drom_df.drop(columns=['title', 'power', 'engine'])
    drom_df.columns = drom_df.columns.str.lower()
    for col in drom_df.columns:
        if col != 'link':
            drom_df[col] = drom_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # print(drom_df[['brand', 'model', 'year', 'price']])
    # print(drom_df[['engine_type', 'engine_volume', 'transmission', 'mileage']])
    # print(drom_df[['body_type', 'drive_type', 'location', 'publication_date']])

    # print(drom_df.dtypes)
    return drom_df