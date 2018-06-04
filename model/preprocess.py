import pandas as pd
from sklearn import preprocessing

def run():
    df = pd.read_csv('output/kl.csv', sep=';')

    # date formating
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # filtering landed/non-landed
    non_landed = ['Flat', 'Condominium/Apartment', 'Hotel/Service Apartment']
    df['is_landed_property'] = [1 if d in non_landed else 0 for d in df['house_type']]

    # making columns become numbers
    df['type_id'] = preprocessing.LabelEncoder().fit_transform(df['house_type'])
    df['addr_id'] = preprocessing.LabelEncoder().fit_transform(df['addr'].astype(str))
    df['neig_id'] = preprocessing.LabelEncoder().fit_transform(df['neighbourhood'])
    df['area_id'] = preprocessing.LabelEncoder().fit_transform(df['area'])
    df['timestamp'] = pd.to_datetime(df['date']).astype(int)

    return df.drop(['house_type', 'addr', 'neighbourhood', 'area', 'date'], axis=1).values