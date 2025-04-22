import pandas as pd
import re
from datetime import datetime



def extract_car_info(title):
    brand = title.split()[0]
    engine_volume_match = re.search(r'\d+\.\d+', title)
    engine_volume = engine_volume_match.group() if engine_volume_match else None
    model = title.split(maxsplit=1)[1].split(engine_volume)[0].strip()
    year = title.split(',')[-2].strip()
    if len(year) != 4:
        return None, None, None, None, None
    mileage_match = re.search(r'(\d{1,3}(?:\s?\d{3})?\s?км)', title)
    if mileage_match:
        mileage = mileage_match.group().replace(' ', '').replace('км', '')
    else:
        mileage = None

    return brand, model, float(engine_volume), int(year), int(mileage) if mileage else None

def transform_transmission(transmission):
    if transmission == 'Механика':
        return 'механическая'
    return 'автоматическая'

def transform_avito_data():
    avito_df = pd.read_json('avito_data.json')

    avito_df[['brand', 'model', 'engine_volume', 'year', 'mileage']] = avito_df['title'].apply(extract_car_info).apply(
        pd.Series)
    avito_df = avito_df.dropna(subset=['brand', 'model', 'engine_volume', 'year', 'mileage'])
    avito_df = avito_df.reset_index(drop=True)
    avito_df['year'] = avito_df['year'].astype(int)
    avito_df['mileage'] = avito_df['mileage'].astype(int)
    avito_df['price'] = avito_df['price'].str.replace(' ', '').str.rstrip('₽').astype(int)
    avito_df['transmission'] = avito_df['transmission'].apply(transform_transmission).apply(pd.Series)
    avito_df['body_type'] = avito_df['body_type'].str.split().str[0]
    avito_df = avito_df.drop(columns=['publication_date', 'title'])
    avito_df['publication_date'] = datetime.now().strftime('%d-%m-%Y')
    avito_df['publication_date'] = pd.to_datetime(avito_df['publication_date'], format='%d-%m-%Y')
    for col in avito_df.columns:
        if col != 'link':
            avito_df[col] = avito_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)

    # print(avito_df[['brand', 'model', 'engine_volume', 'year', 'mileage']])
    # print(avito_df[['price', 'transmission', 'body_type', 'publication_date']])
    # print(avito_df[['engine_type', 'location', 'description']])
    # print(avito_df[['link', 'drive_type']])

    # print(avito_df.dtypes)
    return avito_df
