import json
import msgpack
import os
import numpy as np

def shrek(input_filename, json_output, msgpack_output):

  try:
    with open(input_filename, 'r', encoding='utf-8') as f:
      data = json.load(f)
  except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    return None

  aggregated_data = {}
  for item in data:
    product = item['name']
    price = item['price']
    if product not in aggregated_data:
      aggregated_data[product] = {'prices': []}
    aggregated_data[product]['prices'].append(price)

  results = {}
  for product, item_data in aggregated_data.items():
   prices = np.array(item_data['prices'])
   results[product] = {
     'avg': float(np.mean(prices)),
     'max': float(np.max(prices)),
     'min': float(np.min(prices)),
   }

  with open(json_output, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

  with open(msgpack_output, 'wb') as f:
    msgpack.pack(results, f)

  json_size = os.path.getsize(json_output)
  msgpack_size = os.path.getsize(msgpack_output)
  print(f"Размер JSON файла: {json_size} байт")
  print(f"Размер Msgpack файла: {msgpack_size} байт")
  print(f"JSON больше Msgpack в {json_size / msgpack_size:.2f} раз(а)")


input_file = "data/third_task.json" 
json_output_file = "task3output_json.json"
msgpack_output_file = "task3output_msgpack.msgpack"

shrek(input_file, json_output_file, msgpack_output_file)
