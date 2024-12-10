import sqlite3
import json

def connect_to_db(filename):
  return sqlite3.connect(filename)

def shrek(inputfile, bd_path, output1_json_path, output2_json_path, output_stats_path):

  try:
    with open(inputfile, 'r', encoding='utf-8') as infile:
      lines = infile.readlines()
  except FileNotFoundError:
    print(f"Error: File '{inputfile}' not found.")
    return []
  
  
  #print(lines)
  
  data = []
  tournament_data = {}
  for line in lines:
    line = line.strip()
    #print(line)
    if line == "=====":
      data.append(tuple(tournament_data.values()))
      tournament_data = {}
    elif "::" in line:
      key, value = line.split("::")
      #print(key + " " + value)
      if key =='name':
        year = value.split(' ')[-1]
        tournament_data['name'] = value.replace(year, '').strip()
        tournament_data['year'] = int(year)
      else:
        tournament_data[key] = value
  
  print(data)
  
  conn = connect_to_db(bd_path)
  cursor = conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    year INTEGER,
    city TEXT,
    begin TEXT,
    system TEXT,
    tours_count INTEGER,
    min_rating INTEGER,
    time_on_game INTEGER
      )
  ''')
  conn.commit()

  cursor.executemany('''
    INSERT OR IGNORE INTO tournaments (id, name, year, city, begin, system, tours_count, min_rating, time_on_game)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
  conn.commit()

  cursor.execute("SELECT * FROM tournaments ORDER BY id LIMIT 20 ")
  results = cursor.fetchall()
  for row in results:
      print(row)

  cursor.execute("PRAGMA table_info(tournaments)")
  column_names = [row[1] for row in cursor.fetchall()]
  data = [dict(zip(column_names, row)) for row in results]

  with open(output1_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)


  cursor.execute('''
    SELECT SUM(min_rating), MIN(min_rating), MAX(min_rating), CAST(SUM(min_rating) AS REAL) / COUNT(min_rating)
    FROM tournaments''')
  stats = cursor.fetchall()
  print(stats)

  cursor.execute('''
      SELECT name, COUNT(*) AS shrek
      FROM tournaments
      GROUP BY name
      ORDER BY shrek DESC
    ''')
  name_frequencies = cursor.fetchall()
  print(name_frequencies)
  
  with open(output_stats_path, 'w', encoding='utf-8') as f:
    f.write("Статистика по min_rating:\n")
    f.write('SUM:' + str(stats[0][0]) + "\n") 
    f.write('MIN:' + str(stats[0][1]) + "\n") 
    f.write('MAX:' + str(stats[0][2]) + "\n") 
    f.write('MEAN:' + str(stats[0][3]) + "\n\n") 

    f.write("Частота встречаемости имен турниров:\n")
    for name, count in name_frequencies:
      f.write(f"{name}: {count}\n")

  
  cursor.execute('''
      SELECT id, year, city, system, name, min_rating
      FROM tournaments
      WHERE system = 'Swiss'
      ORDER BY year
      LIMIT 20
    ''')
  Swiss_system = cursor.fetchall()
  
  column_names = ['id', 'year', 'city', 'system', 'name', 'min_rating']
  data = [dict(zip(column_names, row)) for row in Swiss_system]

  with open(output2_json_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  conn.close()


inputfile = "data/1-2/item.text"
bdpath = "task1_2_database.db"

output1_json_path = "task1_output_tournaments.json"
output2_json_path = "task1_output_filtred.json"
output_stats_path = "task1_stats.txt"

shrek(inputfile, bdpath, output1_json_path, output2_json_path, output_stats_path)
