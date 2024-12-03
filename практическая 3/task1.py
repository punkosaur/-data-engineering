import os
import json
import re
from bs4 import BeautifulSoup
from collections import Counter

def parse_html(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()
  soup = BeautifulSoup(html, 'html.parser')
  data = {}

  artikul = soup.find(text=re.compile('Артикул:'))
  artikul = re.sub(r'\s+', '', artikul)
  if artikul: 
    data['Артикул'] = artikul.split(':')[1].strip().replace("Наличие","")
    data['Наличие'] = artikul.split(':')[2]
  else:
    data['Артикул'] = None

  nazvanie = soup.find('h1', class_='title')
  if nazvanie: 
    data['Название'] = nazvanie.text.split(':')[1].strip()
  else:
    data['Название'] = None
    
  adress = soup.find('p', class_='address-price')
  adress = re.sub(r'\s+', '', adress.text)
  if adress: 
    data['Город'] = adress.split(':')[1].strip().replace("Цена","")
    data['Цена (руб)'] = float(adress.split(':')[2].replace("руб",""))
  else:
    data['Город'] = None
    data['Цена (руб)'] = None

  cvet = soup.find('span', class_='color')
  if cvet: 
    data['Цвет'] = cvet.text.split(':')[1].strip()
  else:
    data['Цвет'] = None

  kolichestvo = soup.find('span', class_='quantity')
  if kolichestvo: 
    data['Количество'] = int(kolichestvo.text.split(':')[1].replace("шт",""))
  else:
    data['Количество'] = None

  razmeri = soup.find('span', text=re.compile('Размеры:'))
  if razmeri: 
    data['Размеры'] = razmeri.text.split(':')[1].strip()
  else:
    data['Размеры'] = None
  
  izobrаjenie = soup.find('img')
  if izobrаjenie:
      data['Изображение'] = izobrаjenie.get('src') 
  else:
      data['Изображение'] = None

  reyting = soup.find('span', text=re.compile('Рейтинг:'))
  if reyting: 
    data['Рейтинг'] = float(reyting.text.split(':')[1].strip())
  else:
    data['Рейтинг'] = None

  prosmotri = soup.find('span', text=re.compile('Просмотры:'))
  if prosmotri: 
    data['Просмотры'] = int(prosmotri.text.split(':')[1].strip())
  else:
    data['Просмотры'] = None

  return data

def process_html_files(directory):
  all_data = []
  for filename in os.listdir(directory):
    if filename.endswith(".html"):
      filepath = os.path.join(directory, filename)
      try:
        data = parse_html(filepath)
        all_data.append(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  return all_data


directory = "data/1"
all_data = process_html_files(directory)


# Сохранение в JSON
with open('task1output.json', 'w', encoding='utf-8') as f:
  json.dump(all_data, f, ensure_ascii=False, indent=4)

# Сортировка по названию
sorted_data = sorted(all_data, key=lambda x: x['Название'])
with open('task1output_sorted_by_title.json', 'w', encoding='utf-8') as f:
  json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# Фильтрация по наличию
filtered_data = [item for item in all_data if item['Наличие'] == 'Да']
with open('task1output_filtered_by_availability.json', 'w', encoding='utf-8') as f:
  json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# Статистика по цене
prices = [item['Цена (руб)'] for item in all_data]
price_stats = {
  'сумма': sum(prices),
  'мин': min(prices),
  'макс': max(prices),
  'среднее': sum(prices) / len(prices)
}


# Частота меток цвета
colors = [item['Цвет'] for item in all_data]
color_counts = dict(Counter(colors))

with open('task1output_statistics.txt', 'w', encoding='utf-8') as outfile:
  outfile.write(f"Статистика по цене:, {price_stats}\nЧастота меток цвета: {color_counts}")
