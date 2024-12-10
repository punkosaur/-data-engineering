import sqlite3
import json
import msgpack

def connect_to_db(filename):
  return sqlite3.connect(filename)

def create_db(conn, data):
  
  cursor = conn.cursor()

  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prises'")

  if cursor.fetchone():
    print("Таблица 'prises' уже существует.")
    return 

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS prises (
    name TEXT,
    year INTEGER,
    place INTEGER,
    prise INTEGER
      )
  ''')
  conn.commit()
  print("Таблица 'prises' создана.")

  cursor.executemany('''
    INSERT OR IGNORE INTO prises (name, year, place, prise)
    VALUES (?, ?, ?, ?)
    ''', data)
  conn.commit()

def shrek(inputfile, bd_path, output1_json_path, output2_json_path, output3_json_path):

  try:
    with open(inputfile, 'rb') as f:
      lines = msgpack.unpack(f)
  except Exception as e:
    print(f"Ошибка при чтении файла: {e}")


  data = []
  for line in lines:
    year = line['name'].split(' ')[-1]
    bimba = {
      'name': line['name'].replace(year, '').strip(),
      'year': int(year),
      'place': int(line['place']),
      'prise': int(line['prise'])
    }
    data.append(tuple(bimba.values()))

  conn = connect_to_db(bd_path)
  cursor = conn.cursor()

  create_db(conn, data)

  # проверяю таблицу призов
  cursor.execute("SELECT * FROM prises ORDER BY 1, 2, 3, 4")
  results = cursor.fetchall()
  #for row in results:
  #  print(row)

  # какие есть призы для тех или иных турниров, 
  # турниры без призов и призы без турниров тоже должны отображаться
  cursor.execute('''
  SELECT 
    t.id, t.name, t.year, t.city, t.begin, t.system, t.tours_count, t.min_rating, t.time_on_game, 
    p.place, p.prise
  FROM
    tournaments t
  FULL JOIN
    prises p ON t.name = p.name AND t.year = p.year
  ORDER BY t.name, t.year, p.place, p.prise;
  ''')
  fulljoin = cursor.fetchall()

  column_names = ['id', 'name', 'year', 'city', 'begin', 'system', 'tours_count', 'min_rating', 'time_on_game', 
    'place', 'prise']
  data = [dict(zip(column_names, row)) for row in fulljoin]

  with open(output1_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  # Средний приз за турнир
  cursor.execute('''
  SELECT 
    t.name, t.year, AVG(p.prise) AS average_prise
  FROM 
    tournaments t
  INNER JOIN
    prises p ON t.name = p.name AND t.year = p.year
  GROUP BY
    t.name, t.year
  ORDER BY
    t.year;
  ''')
  average_prise = cursor.fetchall()

  column_names = [ 'name', 'year', 'average_prise']
  data = [dict(zip(column_names, row)) for row in average_prise]

  with open(output2_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  # Турниры, в которых минимальный приз больше порогового значения
  cursor.execute('''
  SELECT
    t.name,
    t.year,
    MIN(p.prise) AS minimal_prise
  FROM
      tournaments t
  INNER JOIN
      prises p ON t.name = p.name AND t.year = p.year
  GROUP BY
      t.name, t.year
  HAVING
      MIN(p.prise) > 1000000
  ORDER BY
      t.year;
  ''')
  minimal_prise = cursor.fetchall()

  column_names = [ 'name', 'year', 'minimal_prise']
  data = [dict(zip(column_names, row)) for row in minimal_prise]

  with open(output3_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  conn.close()
  return

inputfile = "data/1-2/subitem.msgpack"
bdpath = "task1_2_database.db"

output1_json_path = "task2_output_fulljoin.json"
output2_json_path = "task2_output_mean_prise.json"
output3_json_path = "task2_output_minimal_prise.json"

shrek(inputfile, bdpath, output1_json_path, output2_json_path, output3_json_path)