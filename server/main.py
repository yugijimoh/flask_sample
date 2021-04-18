# -*- coding: utf-8 -*

import json
import csv
import pandas as pd


src_file = "../dummy_data/feed_status.csv"

def dfcsv(src_csv):
    csv_data = pd.read_csv(src_csv, low_memory=False)  # 防止弹出警告
    csv_df = pd.DataFrame(csv_data)
    print(csv_df)
    return csv_df

def run_df_csv():
    return dfcsv(src_file)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #csv2json(src_file)
    dfcsv(src_file)

# try git
