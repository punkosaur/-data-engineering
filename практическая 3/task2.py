import os
import json
import re
from bs4 import BeautifulSoup
from collections import Counter

def get_properties(propretis):
  prop = {}
  for p in propretis:
    prop[p['type']] = p.text.strip()
  return prop



def parse_html(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()
  soup = BeautifulSoup(html, 'html.parser')

  products = soup.find_all("div", attrs = {'class': 'product-item'})
  data = []

  for product in products:
    product = products[0]
    item = {}
    item ['id'] = int(product.a['data-id'])
    item ['link'] = product.find_all('a')[1]['href']
    item ['image'] = product.img['src']
    item ['title'] = product.span.text.strip()
    item ['price'] = float(product.price.text.replace('₽', '').replace(' ', '').strip())
    item ['strong'] = int(product.strong.text.replace(' бонусов', '').replace('+ начислим ', '').strip())

    properties = product.ul.find_all('li')
    #print(properties)

    item['properties'] = get_properties(properties)
    data.append(item)
  return data

def process_html_files(directory):
  all_data = []
  for filename in os.listdir(directory):
    if filename.endswith(".html"):
      filepath = os.path.join(directory, filename)
      try:
        data = parse_html(filepath)
        all_data.extend(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  return all_data


directory = "data/2"
all_data = process_html_files(directory)

# Сохранение в JSON
with open('task2output.json', 'w', encoding='utf-8') as f:
  json.dump(all_data, f, ensure_ascii=False, indent=4)


# Сортировка по ИД
sorted_data = sorted(all_data, key=lambda x: x['id'])
with open('task2output_sorted_by_id.json', 'w', encoding='utf-8') as f:
  json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# Фильтрация по цене больше 100к
filtered_data = [item for item in all_data if item['price'] > 100000]
with open('task2output_filtered_by_price.json', 'w', encoding='utf-8') as f:
  json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# Статистика по бонусам
prices = [item['strong'] for item in all_data]
price_stats = {
  'сумма': sum(prices),
  'мин': min(prices),
  'макс': max(prices),
  'среднее': sum(prices) / len(prices)
}

# Частота наименований
names = [item['title'] for item in all_data]
names_counts = dict(Counter(names))

with open('task2output_statistics.txt', 'w', encoding='utf-8') as outfile:
  outfile.write(f"Статистика по бонусам:, {price_stats}\nЧастота наименований: {names_counts}")