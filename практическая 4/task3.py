import csv
import json
import sqlite3

def load_data_csv(csv_filepath):
  data = []
  with open(csv_filepath, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
      row['duration_ms'] = int(row['duration_ms'])
      row['year'] = int(row['year'])
      row['tempo'] = float(row['tempo'])
      row['energy'] = float(row['energy'])
      row['key'] = int(row['key'])
      row['loudness'] = float(row['loudness'])
      data.append(row)
  return data


def load_data_json(json_filepath):
  data = []
  with open(json_filepath, 'r', encoding='utf-8') as file:
    json_data = json.load(file)
    for item in json_data:
      item['duration_ms'] = int(item['duration_ms'])
      item['year'] = int(item['year'])
      item['tempo'] = float(item['tempo'])
      item['explicit'] = item['explicit'] == 'True' # Преобразуем строку в булево значение
      item['popularity'] = int(item['popularity'])
      item['danceability'] = float(item['danceability'])
      data.append(item)
  return data

def create_db(conn, csv_filepath, json_filepath):
  
  cursor = conn.cursor()

  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='songs'")

  if cursor.fetchone():
    print("Таблица 'songs' уже существует.")
    return 

  create_table_sql = """
      CREATE TABLE IF NOT EXISTS songs (
          artist TEXT,
          song TEXT,
          duration_ms INTEGER,
          year INTEGER,
          tempo REAL,
          genre TEXT,
          energy REAL,
          key INTEGER,
          loudness REAL,
          explicit BOOLEAN,
          popularity INTEGER,
          danceability REAL
      )
  """
  cursor = conn.cursor()
  cursor.execute(create_table_sql)
  conn.commit()
  print("Таблица 'songs' создана.")
  
  csv_data = load_data_csv(csv_filepath)
  json_data = load_data_json(json_filepath)

  combined_data = []
  for row in csv_data:
    combined_data.append(
        (row['artist'], row['song'], row['duration_ms'], row['year'], row['tempo'], row['genre'], row['energy'], row['key'], row['loudness'], None, None, None)
    )

  for row in json_data:
    combined_data.append(
        (row['artist'], row['song'], row['duration_ms'], row['year'], row['tempo'], row['genre'], None, None, None, row['explicit'], row['popularity'], row['danceability'])
    )

  cursor.executemany('''
      INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, energy, key, loudness, explicit, popularity, danceability)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  ''', combined_data)
  conn.commit()


def shrek(csv_filepath, json_filepath, db_filepath, output1_json_path, output2_json_path, output_stats_path):
  conn = sqlite3.connect(db_filepath)
  cursor = conn.cursor()
  
  create_db(conn, csv_filepath, json_filepath)

  cursor.execute("SELECT * FROM songs ORDER BY 1, 2, 3, 4")
  results = cursor.fetchall()
  #for row in results:
  #  print(row)

  cursor.execute("SELECT * FROM songs ORDER BY 1, 2, 3, 4 LIMIT 20 ")
  results = cursor.fetchall()

  cursor.execute("PRAGMA table_info(songs)")
  column_names = [row[1] for row in cursor.fetchall()]
  data = [dict(zip(column_names, row)) for row in results]

  with open(output1_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  cursor.execute('''
    SELECT SUM(tempo), MIN(tempo), MAX(tempo), AVG(tempo)
    FROM songs''')
  stats = cursor.fetchall()
  print(stats)

  cursor.execute('''
      SELECT genre, COUNT(*) AS shrek
      FROM songs
      GROUP BY genre
      ORDER BY shrek DESC
    ''')
  name_frequencies = cursor.fetchall()
  print(name_frequencies)
  
  with open(output_stats_path, 'w', encoding='utf-8') as f:
    f.write("Статистика по tempo:\n")
    f.write('SUM:' + str(stats[0][0]) + "\n") 
    f.write('MIN:' + str(stats[0][1]) + "\n") 
    f.write('MAX:' + str(stats[0][2]) + "\n") 
    f.write('MEAN:' + str(stats[0][3]) + "\n\n") 

    f.write("Частота встречаемости жанров песен:\n")
    for name, count in name_frequencies:
      f.write(f"{name}: {count}\n")

  #Сколько песни больше 5ти минут
  cursor.execute('''
      SELECT artist, song, duration_ms, year, tempo, genre
      FROM songs
      WHERE duration_ms > 300000
      ORDER BY year
      LIMIT 25
    ''')
  Swiss_system = cursor.fetchall()
  
  column_names = ['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre']
  data = [dict(zip(column_names, row)) for row in Swiss_system]

  with open(output2_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  conn.close()
  return

csv_filepath = "data/3/_part_1.csv"
json_filepath = "data/3/_part_2.json"
db_filepath = "task3_database.db"


output1_json_path = "task3_output_songs.json"
output2_json_path = "task3_output_filtred.json"
output_stats_path = "task3_stats.txt"

shrek(csv_filepath, json_filepath, db_filepath, output1_json_path, output2_json_path, output_stats_path)