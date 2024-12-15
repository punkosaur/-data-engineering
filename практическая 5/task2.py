import pandas as pd
from pymongo import MongoClient
import json

def db_insert(filepath):

  client = MongoClient('mongodb://localhost:27017/')
  db = client['local']
  collection = db['jobs']
  with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)
    collection.insert_many(data)
  print(f"Данные успешно загружены в MongoDB")

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

  query1 = [
      {
        "$group":{
          "_id": None,
          "max_salary": {"$max": "$salary"},
          "min_salary": {"$min": "$salary"},
          "avg_salary": {"$avg": "$salary"},
        }
      }     
    ]
  
  result1 = list(collection.aggregate(query1))  
  # print("Запрос 1")
  # print(result1)
  save_in_json(result1, 'task2_output1.json')

  query2 = [
      {
        "$group":{
          "_id": "$job",
          "count": {"$sum": 1},
        }
      }     
    ]
  
  result2 = list(collection.aggregate(query2)) 
  # print("Запрос 2")
  # print(result2)
  save_in_json(result2, 'task2_output2.json')

  query3 = [
      {
        "$group":{
          "_id": "$city",
          "max_salary": {"$max": "$salary"},
          "min_salary": {"$min": "$salary"},
          "avg_salary": {"$avg": "$salary"},
        }
      }     
    ]
  
  result3 = list(collection.aggregate(query3)) 
  # print("Запрос 3")
  # print(result3)
  save_in_json(result3, 'task2_output3.json')

  query4 = [
      {
        "$group":{
          "_id": "$job",
          "max_salary": {"$max": "$salary"},
          "min_salary": {"$min": "$salary"},
          "avg_salary": {"$avg": "$salary"},
        }
      }     
    ]
  
  result4 = list(collection.aggregate(query4)) 
  # print("Запрос 4")
  # print(result4)
  save_in_json(result4, 'task2_output4.json')

  query5 = [
      {
        "$group":{
          "_id": "$city",
          "max_age": {"$max": "$age"},
          "min_age": {"$min": "$age"},
          "avg_age": {"$avg": "$age"},
        }
      }     
    ]
  
  result5 = list(collection.aggregate(query5)) 
  # print("Запрос 5")
  # print(result5)
  save_in_json(result5, 'task2_output5.json')

  query6 = [
      {
        "$group":{
          "_id": "$job",
          "max_age": {"$max": "$age"},
          "min_age": {"$min": "$age"},
          "avg_age": {"$avg": "$age"},
        }
      }     
    ]
  
  result6 = list(collection.aggregate(query6)) 
  # print("Запрос 6")
  # print(result6)
  save_in_json(result6, 'task2_output6.json')

  query7 = list(collection.find(limit=1).sort({'age':1, 'salary': -1}))
  save_in_json(query7, 'task2_output7.json')

  query8 = list(collection.find(limit=1).sort({'age':-1, 'salary': 1}))
  save_in_json(query8, 'task2_output8.json')

  query9 = [
      {
        "$match":{
          "salary": {"$gt": 50000}
        }  
      },
      {
        "$group":{
          "_id": "$city",
          "max_age": {"$max": "$age"},
          "min_age": {"$min": "$age"},
          "avg_age": {"$avg": "$age"},
        }
      },
      {
        "$sort":{
          "avg_age": -1,
        }
      }    
    ]
  
  result9 = list(collection.aggregate(query9)) 
  # print("Запрос 9")
  # print(result9)
  save_in_json(result9, 'task2_output9.json')  

  query10 = [
      {
        "$match":{
          'city': 'Санкт-Петербург',
          'job': 'Программист',
          '$or': [
              {'age': {'$gt': 18, '$lt': 25}},
              {'age': {'$gt': 50, '$lt': 60}},
          ]
        }  
      },
      {
        "$group":{
          "_id": "$city",
          "max_salary": {"$max": "$salary"},
          "min_salary": {"$min": "$salary"},
          "avg_salary": {"$avg": "$salary"},
        }
      }, 
    ]
  
  result10 = list(collection.aggregate(query10)) 
  # print("Запрос 10")
  # print(result10)
  save_in_json(result10, 'task2_output10.json')

  query11 = [
      
      {
        "$match":{
          'city': 'Сантьяго-де-Компостела',
          'job': {'$in': ['Программист', 'IT-специалист']},
          'age': {'$gte': 22},
        }  
      },
      {
        "$group":{
          "_id": "$job",
          "max_salary": {"$max": "$salary"},
        }
      },
      {
        "$sort":{
          "max_salary": -1,
        }
      } 
    ]
  
  result11 = list(collection.aggregate(query11)) 
  # print("Запрос 11")
  # print(result11)
  save_in_json(result11, 'task2_output11.json')

#db_insert('data/task_2_item.json')
collection = db_coonect()
go_requests(collection)