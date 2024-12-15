import pandas as pd
from pymongo import MongoClient
import json

def db_insert(filepath):
  try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['local']
    collection = db['jobs']
    data_list = []

    with open(filepath, 'r', encoding='utf-8') as f:
      current_record = {}
      for line in f:
        line = line.strip()
        if line == "=====":
          data_list.append(current_record)
          current_record = {}
        elif "::" in line:
          key, value = line.split("::")
          if key in ['salary', 'id', 'year', 'age']:
            current_record[key] = int(value)
          else:
            current_record[key] = value
    collection.insert_many(data_list)
    print(f"Данные успешно загружены в MongoDB")

  except Exception as e:
    print(f"An unexpected error occurred: {e}")

def db_coonect():

  client = MongoClient('mongodb://localhost:27017/')
  db = client['local']
  collection = db['jobs']
  return collection

def save_in_json(data, filepath):
  
  for doc in data:
    for key, value in doc.items():
        if isinstance(value, object):
            doc[key] = str(value)
            
  with open(filepath, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

def save_before_json(collection):

  before = list(collection.find().sort('id', 1))
  save_in_json(before, 'task3_output_before.json')

def go_requests(collection):

  result = collection.delete_many({"$or": [
    {"salary": {"$lt": 25000}}, 
    {"salary": {"$gt": 175000}}
    ]})
  print(f"Удалено документов (запрос 1): {result.deleted_count}")
  

  result = collection.update_many({}, {"$inc": {"age": 1}})
  print(f"Обновлено документов (запрос 2): {result.modified_count}")

  result = collection.update_many({"job": {"$in": ["Программист", "IT-специалист"]}}, {"$mul": {"salary": 1.05}})
  print(f"Обновлено документов (запрос 3): {result.modified_count}")

  result = collection.update_many({"city": {"$in": ["Краков", "Астана"]}}, {"$mul": {"salary": 1.07}})
  print(f"Обновлено документов (запрос 4): {result.modified_count}")


  result = collection.update_many(
      {"city": "Тбилиси", 
       "job": {"$in": ["Психолог", "Инженер"]}, 
       "age": {"$gte": 30, "$lte": 70}},
      {"$mul": {"salary": 1.10}}
  )
  print(f"Обновлено документов (запрос 5): {result.modified_count}")


  result = collection.delete_many(
      {"city": "Санкт-Петербург", 
       "job": "Психолог", 
      },
  )
  print(f"Удалено психологов из Питера: {result.deleted_count}")

  after = list(collection.find().sort('id', 1))
  save_in_json(after, 'task3_output_after.json')


#db_insert('data/task_3_item.text')
collection = db_coonect()
#save_before_json(collection)
go_requests(collection)