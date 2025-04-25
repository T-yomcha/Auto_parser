import pandas as pd


def extract_car_info(title):
    parts = title.split()
    brand = parts[0]
    model = ' '.join(parts[1:-1]).strip(',')
    year = int(parts[-1].strip(','))
    return brand, model, year

def extract_engine(engine_str):
    if engine_str == 'Неуказано':
        return None, None, None
    engine_volume = float(engine_str[:3])
    power = engine_str.split('/')[1].split('л')[0].replace(' ', '')
    engine_type = engine_str[-6:]
    return engine_volume, power, engine_type

def val_drive_type(drive_type):
    val_value = ['передний', 'задний', 'полный']
    if drive_type not in val_value:
        return None
    return drive_type

def transform_transmission(transmission):
    if transmission == 'механическая':
        return transmission
    return 'автоматическая'

def extract_publication(publication_date):
    dates = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04',
        'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
        'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    }
    if len(publication_date) < 11:
        publication_date = publication_date+' 2025'
    for month_name, month_number in dates.items():
        publication_date = publication_date.replace(month_name, month_number)
    publication_date = publication_date.replace(' ', ':')
    return publication_date

def transform_autoru_data():
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
        >>> df = transform_autoru_data()
        >>> print(df.columns)
        Index(['brand', 'model', 'year', 'price', 'engine_volume', 'engine_type',
               'body_type', 'drive_type', 'transmission', 'mileage', 'location',
               'publication_date', 'description', 'link'],
              dtype='object')
    """
    autoru_df = pd.read_json('autoru_data.json')

    autoru_df[['brand', 'model', 'year']] = autoru_df['title'].apply(extract_car_info).apply(pd.Series)
    autoru_df['price'] = autoru_df['price'].str.replace(' ', '').str.rstrip('₽').astype(int)
    autoru_df['engine_type'] = autoru_df['engine_type'].str.replace(' ', '')
    autoru_df[['engine_volume', 'power', 'engine_type']] = autoru_df['engine_type'].apply(extract_engine).apply(
        pd.Series)
    autoru_df['body_type'] = autoru_df['body_type'].str.split().str[0]
    autoru_df['drive_type'] = autoru_df['drive_type'].apply(val_drive_type).apply(pd.Series)
    autoru_df['transmission'] = autoru_df['transmission'].apply(transform_transmission).apply(pd.Series)
    autoru_df['publication_date'] = autoru_df['publication_date'].apply(extract_publication).apply(pd.Series)
    autoru_df['publication_date'] = pd.to_datetime(autoru_df['publication_date'], format='%d:%m:%Y', errors='coerce')

    autoru_df = autoru_df.dropna(subset=['engine_type', 'drive_type'])
    autoru_df = autoru_df.reset_index(drop=True)
    autoru_df['power'] = autoru_df['power'].astype(int)
    autoru_df.columns = autoru_df.columns.str.lower()
    for col in autoru_df.columns:
        if col != 'link':
            autoru_df[col] = autoru_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
    autoru_df['mileage'] = autoru_df['mileage'].str.replace(' ', '').str.replace(r'[^0-9]', '', regex=True).astype(int)
    autoru_df = autoru_df.drop(columns=['title', 'power'])

    # print(autoru_df[['brand', 'model', 'year', 'price']])
    # print(autoru_df[['engine_volume', 'engine_type', 'body_type']])
    # print(autoru_df[['drive_type', 'transmission', 'publication_date', 'location', 'mileage']])
    # print(autoru_df[['description', 'link']])
    # print(autoru_df.dtypes)
    return autoru_df