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


def parse_one_page_html(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()
  soup = BeautifulSoup(html, 'html.parser')

  item = {}
  item['title'] = soup.find('h1', class_='product_title entry-title').text
  item['bonus'] = int(re.sub(r'[^\d.]', '',soup.find('span', class_='wps_wpr_product_point').text))
  rate_tag = soup.find('div', class_='star-rating')
  if rate_tag is None:
      item['review'] = None
      item['rating'] = None
  elif 'Рейтинг' in rate_tag.text:
    item['review'] = int(re.sub(r'[^\d.]', '',rate_tag.text.split('опроса')[1].replace('пользователя', '')))
    item['rating'] = float(re.sub(r'[^\d.]', '',rate_tag.text.split('из')[0]))
  else:
    item['review'] = None
    item['rating'] = None
  item ['price'] = float(soup.find('span', class_='woocommerce-Price-amount amount').text.replace('₽','').replace(',','.').strip())
  item ['description'] = soup.find('div', class_='woocommerce-product-details__short-description').text.replace('\n','')

  return item

def parse_catalog_html(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()
  soup = BeautifulSoup(html, 'html.parser')

  products = soup.find_all('div', class_='thunk-product-wrap')
  items = []
  for product in products:
    item = {}
    item['title'] = product.find('h2', class_='woocommerce-loop-product__title').text.strip() 
    #print(item['title'])
    item['price'] = float(product.find('span', class_='woocommerce-Price-amount amount').text.replace(',', '.').replace('₽','').strip())
    
    rate_tag = product.find('div', class_='star-rating')
    if rate_tag is None:
        item['rating'] = None
    
    elif rate_tag['aria-label']:
      item['rating'] = float(re.sub(r'[^\d.]', '',rate_tag['aria-label'].split('из')[0]))
    
    items.append(item)
    

  return items

def process_html_files(one_page_directory, catalogs_directory):
  all_data = []
  for filename in os.listdir(one_page_directory):
    if filename.endswith(".html"):
      filepath = os.path.join(one_page_directory, filename)
      try:
        data = parse_one_page_html(filepath)
        all_data.append(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
  
  for filename in os.listdir(catalogs_directory):
    if filename.endswith(".html"):
      filepath = os.path.join(catalogs_directory, filename)
      try:
        data = parse_catalog_html(filepath)
        all_data.extend(data)
      except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
      
  return all_data


one_page_directory = "syte/single pages"
catalogs_directory = "syte/catalogs"
all_data = process_html_files(one_page_directory, catalogs_directory)

# Сохранение в JSON
with open('task5output.json', 'w', encoding='utf-8') as f:
  json.dump(all_data, f, ensure_ascii=False, indent=4)


# Сортировка по наимнованию
sorted_data = sorted(all_data, key=lambda x: x['title'])
with open('task5output_sorted_by_title.json', 'w', encoding='utf-8') as f:
  json.dump(sorted_data, f, ensure_ascii=False, indent=4)

# Фильтрация по цене больше 10к
filtered_data = [item for item in all_data if item['price'] > 10000]
with open('task5output_filtered_by_price.json', 'w', encoding='utf-8') as f:
  json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# Статистика по цене
prices = [item['price'] for item in all_data]
price_stats = {
  'сумма': sum(prices),
  'мин': min(prices),
  'макс': max(prices),
  'среднее': sum(prices) / len(prices)
}

# Частота оценок в рейтинге 
names = [item['rating'] for item in all_data]
names_counts = dict(Counter(names))

with open('task5output_statistics.txt', 'w', encoding='utf-8') as outfile:
  outfile.write(f"Статистика по цене:, {price_stats}\nЧастота оценок в рейтинге (это не строка, но интересно что будет, я вроде видел только по 5 завезд и без оценок): {names_counts}")
