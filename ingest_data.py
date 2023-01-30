import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
# user, password, host, port, database name, table name
# url of CSV

def main(params):
    user = params.user
    password = params.password
    host=params.host
    port=params.port
    db=params.db
    table_name=params.table_name
    url=params.url

    csv_name='output.csv'
    os.system(f'wget -O {csv_name} {url}')
    
    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name,iterator=True, chunksize=100000)
    df=next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    while True:
        t_start = time()
        df=next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine ,if_exists='append')
        t_end=time()

        print("inserted another chunk, took .%3f seconds" %(t_end-t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')

    parser.add_argument('--user', help='username')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres hostname')
    parser.add_argument('--port', help='postgres port')
    parser.add_argument('--db', help='postgres database')
    parser.add_argument('--table_name', help='database table name')
    parser.add_argument('--url', help='csv url')

    args=parser.parse_args()
    main(args)

  




