import pandas as pd
import json
import os
import numpy as np
import csv
import msgpack
import pickle

def shrek(dataset_path, csv_path, json_path, msgpack_path, pkl_path, comparison_output_file):
  try:
    df = pd.read_csv(dataset_path)
  except FileNotFoundError:
    print(f"Error: File '{dataset_path}' not found.")
    return None

  cols = ['brewery_name', 'beer_style', 'beer_name',
          'review_time', 'review_overall', 'review_aroma', 'review_appearance', 'review_profilename', 'review_palate', 'review_taste']
  extracted_df = df[cols]
  #print(extracted_df.head())

  numerical_cols = ['review_time', 'review_overall', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste']
  text_cols = ['brewery_name', 'beer_style', 'beer_name', 'review_profilename']

  stats = {}
  for col in numerical_cols:
    if pd.api.types.is_numeric_dtype(df[col]):
      stats[col] = {
        'max': float(df[col].max()),
        'min': float(df[col].min()),
        'agv': float(df[col].mean()),
        'sum': float(df[col].sum()),
        'std': float(df[col].std()),
      }

  for col in text_cols:
    stats[col] = df[col].value_counts().to_dict()

  extracted_df.to_csv(csv_path, index=False)

  data_dict = extracted_df.to_dict(orient='records')

  with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, indent=4)

  with open(msgpack_path, 'wb') as f:
    msgpack.pack(data_dict, f)

  with open(pkl_path, 'wb') as f:
    pickle.dump(extracted_df, f)

  file_sizes = {
    "csv": os.path.getsize(csv_path),
    "json": os.path.getsize(json_path),
    "msgpack": os.path.getsize(msgpack_path),
    "pickle": os.path.getsize(pkl_path),
  }

  results = {
    'statistics': stats,  # Статы по датасету
    'file_sizes': file_sizes # Размеры файлов
  }

  with open(comparison_output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4)

def barmitzvah(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return

    reduced_df = df[::6]
    reduced_df.to_csv(filepath, index=False)
    print(f"Обрезан и сохранен")

def barmitzvah2(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return
    
    percentage = 16

    num_rows = len(df)
    num_rows_to_keep = int(num_rows * (percentage / 100))

    reduced_df = df.head(num_rows_to_keep)
    reduced_df.to_csv(filepath, index=False)
    print(f"Обрезан и сохранен")

#csv, json, msgpack, pkl
dataset_path = "dataset/beer_reviews.csv"#тут надо рар распаковать

csv_path = "task5output_csv.csv"
json_path = "task5output_json.json"
msgpack_path = "task5output_msgpack.msgpack"
pkl_path = "task5output_pkl.pkl"

comparison_output_file = "task5output_comparisonjson.json"

#barmitzvah2(dataset_path)

shrek(dataset_path, csv_path, json_path, msgpack_path, pkl_path, comparison_output_file)


