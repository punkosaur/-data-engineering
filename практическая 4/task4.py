import sqlite3
import json
import pickle

def connect_to_db(filename):
  return sqlite3.connect(filename)

def handle_updates(conn, updates):

  cursor = conn.cursor()

  for item in updates:
    # print('\n')
    # print(item)
    # print(item['param'])
    # print(item['method'])
    # print(item['name'])
    # print((item['param'], item['name']))
    try:
      if (item['method'] == 'remove'):
        cursor.execute("DELETE FROM products WHERE name = ?", (item['name'],))

      elif (item['method'] == 'price_percent'):
        cursor.execute('''
                      UPDATE products
                      SET price = ROUND(price * (1 + ?), 2),
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))
        

      elif (item['method'] == 'price_abs'):
        cursor.execute('''
                      UPDATE products
                      SET price = price + ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))

      elif (item['method'] == 'quantity_sub' or item['method'] == 'quantity_add'):
        cursor.execute('''
                      UPDATE products
                      SET quantity = quantity + ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))

      elif (item['method'] == 'available'):
        cursor.execute('''
                      UPDATE products
                      SET isAvailable = ?,
                          version = version + 1 
                      WHERE name = ?''', (item['param'], item['name']))
        
      conn.commit()

    except Exception as e:
      print(f"Произошла ошибка: {e}")

def analyze_data(conn):
    cursor = conn.cursor()

    results = {}

    cursor.execute('''SELECT name, version 
                   FROM products 
                   ORDER BY version DESC 
                   LIMIT 10''')
    top_10_updated = cursor.fetchall()
    results["топ-10 самых обновляемых товаров"] = top_10_updated

    cursor.execute('''
        SELECT 
            category, 
            SUM(price) AS sum_price, 
            MIN(price) AS min_price, 
            MAX(price) AS max_price, 
            AVG(price) AS avg_price,
            COUNT(*) AS num_products
        FROM products
        GROUP BY category
    ''')
    price_analysis = cursor.fetchall()
    results["анализ цен по категориям"] = price_analysis

    cursor.execute('''
        SELECT 
            category, 
            SUM(quantity) AS total_quantity, 
            MIN(quantity) AS min_quantity, 
            MAX(quantity) AS max_quantity, 
            AVG(quantity) AS avg_quantity,
            COUNT(*) AS num_products
        FROM products
        GROUP BY category
    ''')
    quantity_analysis = cursor.fetchall()
    results["анализ остатков по категориям"] = quantity_analysis

    cursor.execute('''
                   SELECT name, price 
                   FROM products 
                   WHERE price < 100 AND fromCity = 'Минск' ''')
    my_query = cursor.fetchall()
    results["Минские товары дешевле 100 рублей"] = my_query
    return results

def create_db(conn, inputfile1):
  
  cursor = conn.cursor()

  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")

  if cursor.fetchone():
    print("Таблица 'products' уже существует.")
    return 
  
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
    name TEXT PRIMARY KEY,
    price INTEGER  CHECK (price >= 0.01),
    quantity INTEGER  CHECK (quantity >= 0),
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER,
    category TEXT,
    version INTEGER DEFAULT 0
      )
  ''')
  conn.commit()
  print("Таблица 'products' создана.")
  
  try:
    with open(inputfile1, 'r', encoding='utf-8') as infile:
      lines = infile.readlines()
  except FileNotFoundError:
    print(f"Error: File '{inputfile1}' not found.")
    return []
  
  
  #print(lines)
  
  data = []
  product_data = {}
  product_data['category'] = None
  product_data['price'] = None
  product_data['quantity'] = None
  product_data['fromCity'] = None
  product_data['isAvailable'] = None
  product_data['views'] = None
  for line in lines:
    line = line.strip()
    if line == "=====":
      data.append(tuple(product_data.values()))
      product_data = {}
      product_data['category'] = None
      product_data['price'] = None
      product_data['quantity'] = None
      product_data['fromCity'] = None
      product_data['isAvailable'] = None
      product_data['views'] = None
    elif "::" in line:
      key, value = line.split("::")
      product_data[key] = value
  #print(data)
  
  cursor.executemany('''
    INSERT OR IGNORE INTO products (category, price, quantity, fromCity, isAvailable, views, name)
    VALUES (?, ?, ?, ?, ?, ?, ?)
                     
    ''', data)
  conn.commit()


def shrek(inputfile1, inputfile2, bd_path, output_stats_path):
  conn = connect_to_db(bd_path)
  create_db(conn, inputfile1)
  cursor = conn.cursor()

  try:
    with open(inputfile2, 'rb') as f:
      updates = pickle.load(f)
  except Exception as e:
    print(f"Произошла ошибка: {e}")
  
  handle_updates(conn, updates)

  '''
  cursor.execute("SELECT * FROM products ORDER BY 1")
  results = cursor.fetchall()
  for row in results:
      print(row)

  cursor.execute("PRAGMA table_info(products)")
  column_names = [row[1] for row in cursor.fetchall()]
  print(column_names)
  '''

  results = analyze_data(conn)

  with open(output_stats_path, "w", encoding="utf-8") as f:
    for section, data in results.items():
      f.write(f"\n--- {section.upper()} ---\n")
      if section.upper() == "ТОП-10 САМЫХ ОБНОВЛЯЕМЫХ ТОВАРОВ":
                    header = ["Наименование", "Версия"]
      elif section.upper() == "АНАЛИЗ ЦЕН ПО КАТЕГОРИЯМ":
                    header = ["Категория", "Сумма(цена)", "Минимум(цена)", "Максимум(цена)", "Среднее(цена)", "Количество"]
      elif section.upper() == "АНАЛИЗ ОСТАТКОВ ПО КАТЕГОРИЯМ":
                    header = ["Категория", "Сумма(остатки)", "Минимум(остатки)", "Максимум(остатки)", "Среднее(остатки)", "Количество"]
      elif section.upper() == "МИНСКИЕ ТОВАРЫ ДЕШЕВЛЕ 100 РУБЛЕЙ":
                    header = ["Наименование", "Цена"]
      else:
          header = [] #Обработка неизвестных секций

      # Выводим заголовок
      f.write("".join(f"{h:<25}" for h in header) + "\n")

      #Выводим данные, выравнивая значения влево
      for row in data:
          f.write("".join(f"{str(item):<25}" for item in row) + "\n")




  #for upd in updates:
  #  print(upd)
  #  print('\n')

  conn.close()


inputfile1 = "data/4/_product_data.text"
inputfile2 = "data/4/_update_data.pkl"
bdpath = "task4_database.db"

output_stats_path = "task4_stats.txt"

shrek(inputfile1, inputfile2, bdpath, output_stats_path)
