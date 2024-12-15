import pandas as pd
from pymongo import MongoClient
import json

def db_coonect():

  client = MongoClient('mongodb://localhost:27017/')
  db = client['local']
  collection = db['beer']
  return collection

def db_insert(filepath_csv, filepath_json):
  try:
    collection = db_coonect()

    df = pd.read_csv(filepath_csv, sep=',')
    data = df.to_dict('records')
    collection.insert_many(data)
    print("Данные из csv успешно загружены в MongoDB.")

    with open(filepath_json, 'r', encoding='utf-8') as f:
      data = json.load(f)
      collection.insert_many(data)
    print(f"Данные из json успешно загружены в MongoDB")

  except Exception as e:
    print(f"An unexpected error occurred: {e}")

def save_before_json(collection):

  before = list(collection.find().sort('id', 1))
  save_in_json(before, 'task4_output_before.json')

def save_in_json(data, filepath):
  
  for doc in data:
    for key, value in doc.items():
        if isinstance(value, object):
            doc[key] = str(value)
            
  with open(filepath, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

def go_requests(collection):

  #1 Все пива от Black Sheep и Amstel
  result = list(collection.find({'brewery_name': 
                                 {'$in': ['Black Sheep Brewery PLC', 'Amstel Brouwerij B. V.']}
                                 }))
  save_in_json(result, 'task4_output_1_1.json')
  
  #2 Пиво с рейтингом больше 4
  result = list(collection.find({"review_overall": {"$gt": 4}}))
  save_in_json(result, 'task4_output_1_2.json')

  #3 Все ирлагдские стауты с рейтингом больше 4
  result = list(collection.find({"beer_style": "Irish Stout",
                                 "review_overall": {"$gt": 4}}))
  save_in_json(result, 'task4_output_1_3.json')

  #4 Пиво со вкусом больше 4.3 и хапаъом меньше 3.7
  result = list(collection.find({"review_taste": {"$gt": 4.3}, 
                                 "review_aroma": {"$lt": 3.7}}))
  save_in_json(result, 'task4_output_1_4.json')

  #5 первые 5 видов пива, оцененные больше чем на 4.7
  result = list(collection.find({"review_overall": {"$gt": 4.7}}).sort("review_time", 1).limit(5))
  save_in_json(result, 'task4_output_1_5.json')



  #1 Средний рейтинг пивоварен
  query = [
      {"$group": 
       {"_id": "$brewery_name", 
        "avg_rating": {"$avg": "$review_overall"}}}
  ]
  result = list(collection.aggregate(query))
  save_in_json(result, 'task4_output_2_1.json')


  #2 Количество пива для каждого сорта
  query = [
      {"$group": 
       {"_id": "$beer_style", 
        "count": {"$sum": 1}}}
  ]
  result = list(collection.aggregate(query))
  save_in_json(result, 'task4_output_2_2.json')

  #3  Минимум, Максимум и Средний review_palate для каждого пивовара (brewery_name)
  query = [
      {
        "$group":{
          "_id": "$brewery_name",
          "max_palate": {"$max": "$review_palate"},
          "min_palate": {"$min": "$review_palate"},
          "avg_palate": {"$avg": "$review_palate"},
        }
      },
      {
        "$sort":{
          "max_palate": -1,
        }
      } 
  ]
  result = list(collection.aggregate(query))
  save_in_json(result, 'task4_output_2_3.json')

  #4 Минимум, Максимум и Средний рейтинг для сорта пива
  query = [
      {
        "$group":{
          "_id": "$beer_style",
          "max_overall": {"$max": "$review_overall"},
          "min_overall": {"$min": "$review_overall"},
          "avg_overall": {"$avg": "$review_overall"},
        }
      },
      {
        "$sort":{
          "avg_overall": -1,
        }
      } 
  ]
  result = list(collection.aggregate(query))
  save_in_json(result, 'task4_output_2_4.json')

  #5 Топ 10 ревьюеров по количеству отзывов
  query = [
      {"$group": {
         "_id": "$review_profilename", 
         "review_count": {"$sum": 1}
         }
      },
      {"$sort": {
         "review_count": -1
         }
      },
      {"$limit": 10} 
  ]
  result = list(collection.aggregate(query))
  save_in_json(result, 'task4_output_2_5.json')

  #1 Увеличить рейтинг на 0.1 для низкоалкогольных пив
  query = {"beer_style": "Low Alcohol Beer"}
  update = {"$inc": {"review_overall": 0.1}}
  result = collection.update_many(query, update)
  print(f"Запрос 1: Обновлено {result.modified_count} документов.")

  #2 Удалить все пиво от пивоварни "Brouwerij Verhaeghe",  review_overall которого меньше 4
  query = {"brewery_name": "Brouwerij Verhaeghe", "review_overall": {"$lt": 4}}
  result = collection.delete_many(query)
  print(f"Запрос 2: Удалено {result.deleted_count} документов.")

  #3 Установить рейтинг равным 100500 для кваса
  query = {"beer_style": "Kvass"}
  update = {"$set": {"review_overall": 100500}}
  result = collection.update_many(query, update)
  print(f"Запрос 3: Обновлено {result.modified_count} документов.")

  #4 Уменьшить review_palate на 3% для всех пива стиля "American Pale Ale (APA)",  от пивоварни "West Virginia Brewing Company" с оценкой не меньше 4.
  query = {"beer_style": "American Pale Ale (APA)", 
           "brewery_name": "West Virginia Brewing Company", 
           "review_overall": {"$gte": 4}}
  update = {"$mul": {"review_palate": 0.97}} 
  result = collection.update_many(query, update)
  print(f"Запрос 4: Обновлено {result.modified_count} документов.")


  #5 Удалить все записи, где имя критика содержит "test" И стиль пива это "Flanders Red Ale"
  query = {"review_profilename": {"$regex": "man"}, "beer_style": "Flanders Red Ale"}
  result = collection.delete_many(query)
  print(f"Запрос 5: Удалено {result.deleted_count} документов.")

  after = list(collection.find().sort('id', 1))
  save_in_json(after, 'task4_output_after.json')




db_insert('dataset/beer_reviews.csv', 'dataset/breweries.json')
collection = db_coonect()
save_before_json(collection)
go_requests(collection)