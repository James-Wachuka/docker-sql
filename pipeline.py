import pandas as pd
#import sys
import os
import argparse

def main(params):
    csv_name='output.csv'
    url=params.url
    os.system(f'wget -O {csv_name}  {url}')
    df=pd.read_csv('output.csv', nrows=50)
    print(df)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description="test export to csv")
    parser.add_argument('--url', help='csv url')

    args=parser.parse_args()
    main(args)