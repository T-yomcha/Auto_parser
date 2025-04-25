import pandas as pd
from datetime import datetime


def extract_car_info(title):
    parts = title.split()
    brand = parts[0]
    model = ' '.join(parts[1:-1]).strip(',')
    year = int(parts[-1].strip(','))
    return brand, model, int(year)

def extract_price(price):
    parts = price.split()
    return "".join(parts)

def extract_engine_type(fuel):
    if fuel not in ['Бензиновый', 'Дизельный']:
        return None
    if fuel == 'Бензиновый':
        return 'бензин'
    if fuel == 'Дизельный':
        return 'дизель'

def extract_engine_volume(engine_volume):
    has_digit = any(char.isdigit() for char in engine_volume)
    if has_digit:
        return float(engine_volume[:-2])
    return None

def extract_transmission(transmission):
    if transmission == 'Механика':
        return 'механическая'
    return 'автоматическая'

def extract_publication(publication_date):
    dates = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04',
        'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
        'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    }
    if len(publication_date) < 11 and publication_date != 'Не указано':
        publication_date = publication_date+' 2025'
        for month_name, month_number in dates.items():
            publication_date = publication_date.replace(month_name, month_number)
        publication_date = publication_date.replace(' ', '-')
        return publication_date
    if publication_date == 'Не указано':
        return None
    return datetime.now().strftime('%d-%m-%Y')

def transform_youla_data():
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
        >>> df = transform_youla_data()
        >>> print(df.columns)
        Index(['brand', 'model', 'year', 'price', 'engine_volume', 'engine_type',
               'body_type', 'drive_type', 'transmission', 'mileage', 'location',
               'publication_date', 'description', 'link'],
              dtype='object')
    """
    youla_df = pd.read_json('youla_data.json')

    youla_df['title'] = youla_df['title'].replace('Не указано', None)
    youla_df.dropna(subset=['title'], inplace=True)
    youla_df[['brand', 'model', 'year']] = youla_df['title'].apply(extract_car_info).apply(pd.Series)
    youla_df['price'] = youla_df['price'].apply(extract_price).apply(pd.Series).astype(int)
    youla_df['engine_type'] = youla_df['fuel'].apply(extract_engine_type).apply(pd.Series)
    youla_df['engine_volume'] = youla_df['engine_volume'].apply(extract_engine_volume)
    youla_df['transmission'] = youla_df['transmission'].apply(extract_transmission).apply(pd.Series)
    youla_df['mileage'] = youla_df['mileage'].replace('Не указано', None)
    youla_df.dropna(subset=['mileage'], inplace=True)
    youla_df['mileage'] = youla_df['mileage'].apply(lambda x: x[:-2]).apply(pd.Series).astype(int)
    youla_df['location'] = youla_df['location'].apply(lambda x: 'москва').apply(pd.Series)
    youla_df['publication_date'] = youla_df['publication_date'].apply(extract_publication).apply(pd.Series)
    youla_df['publication_date'] = pd.to_datetime(youla_df['publication_date'], format='%d-%m-%Y', errors='coerce')
    youla_df = youla_df.drop(columns=['title', 'power', 'fuel'])
    youla_df.columns = youla_df.columns.str.lower()
    for col in youla_df.columns:
        if col != 'link':
            youla_df[col] = youla_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # print(youla_df[['brand', 'model', 'year', 'price', 'engine_type']])
    #print(youla_df[['engine_volume', 'transmission', 'mileage', 'body_type', 'drive_type']])
    # print(youla_df[['location', 'publication_date']])

    # print(youla_df.dtypes)
    return youla_df

if __name__ == '__main__':
    transform_youla_data()
