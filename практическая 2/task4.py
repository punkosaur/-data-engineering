import pickle
import json

def shrek(pkl_filename, json_filename, output_filename):
  try:
    with open(pkl_filename, 'rb') as f:
      products = pickle.load(f)
  except FileNotFoundError:
    print(f"Error: File '{pkl_filename}' not found.")
    return None
  
  try:
    with open(json_filename, 'r', encoding='utf-8') as f:
      update = json.load(f)
  except FileNotFoundError:
    print(f"Error: File '{json_filename}' not found.")
    return None

  for product in products:
    #print(product)
    name = product['name']
    price = product['price']
    instruction = next((item for item in update if item['name'] == name), None)
    if instruction:
      method = instruction['method']
      param = instruction['param']
      #print(method)
      #print(param)

      if method == "add":
        price += param
      elif method == "sub":
        price -= param
      elif method == "percent+":
        price *= (1 + param)
      elif method == "percent-":
        price *= (1 - param)
      else:
        print(f"Warning: Unknown method '{method}' for product '{name}'.")
      product['price'] = price
    #print(product)


  with open(output_filename, 'wb') as f:
    pickle.dump(products, f)
  return products


pkl_file = "data/fourth_task_products.json"
json_file = "data/fourth_task_updates.json"
output_file = 'task4output.pkl'

shrek(pkl_file, json_file, output_file)