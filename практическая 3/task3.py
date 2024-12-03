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
  star = BeautifulSoup(xml, 'xml').star

  item = {}
  for el in star:
    if el.name is not None:
      item[el.name] = el.text.strip()
  item['radius'] = int(item['radius'])
  #print(item)
  return item


def process_html_files(directory):
  all_data = []
  for filename in os.listdir(directory):
    if filename.endswith(".xml"):
      filepath = os.path.join(directory, filename)
      try:
        data = parse(filepath)
        all_data.append(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  return all_data


directory = "data/3"
all_data = process_html_files(directory)

# Сохранение в JSON
with open('task3output.json', 'w', encoding='utf-8') as f:
  json.dump(all_data, f, ensure_ascii=False, indent=4)


# Сортировка по Названию
sorted_data = sorted(all_data, key=lambda x: x['name'])
with open('task3output_sorted_by_name.json', 'w', encoding='utf-8') as f:
  json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# Фильтрация по спектральному классу
filtered_data = [item for item in all_data if item['spectral-class'] == 'Q8Q']
with open('task3output_filtered_by_spectral_class.json', 'w', encoding='utf-8') as f:
  json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# Статистика по радиусу
prices = [item['radius'] for item in all_data]
price_stats = {
  'сумма': sum(prices),
  'мин': min(prices),
  'макс': max(prices),
  'среднее': sum(prices) / len(prices)
}

# Частота меток созвездий
names = [item['constellation'] for item in all_data]
names_counts = dict(Counter(names))

with open('task3output_statistics.txt', 'w', encoding='utf-8') as outfile:
  outfile.write(f"Статистика по радиусам:, {price_stats}\nЧастота меток созвездий: {names_counts}")
