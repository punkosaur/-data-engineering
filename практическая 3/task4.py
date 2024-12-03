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


def parse(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    xml = f.read()
  clothings = BeautifulSoup(xml, 'xml').find_all("clothing")
  items = []
  for clothing in clothings:
    item = {}
    item['id'] = int(clothing.id.text.strip())
    item['name'] = clothing.find_all('name')[0].text.strip()
    item['category'] = clothing.category.text.strip()
    item['size'] = clothing.size.text.strip()
    item['color'] = clothing.color.text.strip()
    item['material'] = clothing.material.text.strip()
    item['price'] = float(clothing.price.text.strip())
    item['rating'] = float(clothing.rating.text.strip())
    item['reviews'] = int(clothing.reviews.text.strip())
    sporty_tag = clothing.sporty
    if sporty_tag:
      item['sporty'] = sporty_tag.text.strip() == 'yes'
    new_tag = clothing.new
    if new_tag:
      item['new'] = new_tag.text.strip() == '+'
    exclusive_tag = clothing.new
    if exclusive_tag:
      item['exclusive'] = new_tag.text.strip() == 'yes'

    items.append(item)
  return items


def process_html_files(directory):
  all_data = []
  for filename in os.listdir(directory):
    if filename.endswith(".xml"):
      filepath = os.path.join(directory, filename)
      try:
        data = parse(filepath)
        all_data.extend(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  return all_data


directory = "data/4"
all_data = process_html_files(directory)

# Сохранение в JSON
with open('task4output.json', 'w', encoding='utf-8') as f:
  json.dump(all_data, f, ensure_ascii=False, indent=4)


# Сортировка по Названию
sorted_data = sorted(all_data, key=lambda x: x['name'])
with open('task4output_sorted_by_name.json', 'w', encoding='utf-8') as f:
  json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# Фильтрация по цвету
filtered_data = [item for item in all_data if item['color'] == 'Желтый']
with open('task4output_filtered_by_color.json', 'w', encoding='utf-8') as f:
  json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# Статистика по рейтингу
prices = [item['rating'] for item in all_data]
price_stats = {
  'сумма': sum(prices),
  'мин': min(prices),
  'макс': max(prices),
  'среднее': sum(prices) / len(prices)
}

# Частота меток цветов
names = [item['color'] for item in all_data]
names_counts = dict(Counter(names))

with open('task4output_statistics.txt', 'w', encoding='utf-8') as outfile:
  outfile.write(f"Статистика по рейтингу:, {price_stats}\nЧастота меток цветов: {names_counts}")
