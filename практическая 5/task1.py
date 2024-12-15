import pandas as pd
from pymongo import MongoClient
import json


def db_insert(filepath):

  client = MongoClient('mongodb://localhost:27017/')
  db = client['local']
  collection = db['jobs']

  df = pd.read_csv(filepath, sep=';')
  data = df.to_dict('records')
  collection.insert_many(data)
  print("Данные успешно загружены в MongoDB.")

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

def go_requests(collection):

  # Первые 10, отсортированных по убыванию salary
  query1 = list(collection.find().sort('salary', -1).limit(10))
  #print('Первые 10, отсортированных по убыванию salary')  
  # for q in query1:
  #   print(q)

  save_in_json(query1, 'task1_output1.json')

  # Первые 15 моложе 30, отсортированных по убыванию salary
  query2 = list(collection.find({'age': {'$lt': 30}}).sort('salary', -1).limit(15))
  # print('Первые 15 моложе 30, отсортированных по убыванию salary') 
  # for q in query2:
  #   print(q)

  save_in_json(query2, 'task1_output2.json')

  # Первые 10 из Питера трех разных профессий, отсортированных по ВОЗРАСТанию
  query3 = list(collection.find(
      { 'city': 'Санкт-Петербург',
        'job': {'$in': ['Программист', 'IT-специалист', 'Врач']}
      }
  ).sort('age', 1).limit(10))
  # print('Первые 10 из Питера трех разных профессий, отсортированных по ВОЗРАСТанию')  
  # for q in query3:
  #   print(q)

  save_in_json(query3, 'task1_output3.json')

  # Количество записей по фильтру
  query4 = collection.count_documents(
      {
          'age': {'$gte': 22, '$lte': 52},
          'year': {'$gte': 2019, '$lte': 2022},
          '$or': [
              {'salary': {'$gt': 50000, '$lte': 75000}},
              {'salary': {'$gt': 125000, '$lt': 150000}},
          ],
      }
  )
  
  with open('task1_output4.json', 'w', encoding='utf-8') as f:
    json.dump(query4, f, ensure_ascii=False, indent=4)

#db_insert('data/task_1_item.csv')
collection = db_coonect()
go_requests(collection)