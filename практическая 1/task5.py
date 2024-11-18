from bs4 import BeautifulSoup
import csv

def process_file(input_filename, output_filename):

    try:
      with open(input_filename, 'r', encoding='utf-8') as f:
        html = f.read()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'product-table'})

    rows = table.find_all('tr')
    header = [th.text.strip() for th in rows[0].find_all('th')]
    data = []

    for row in rows[1:]: #Skip header row
      cols = row.find_all('td')
      data.append([col.text.strip() for col in cols])


    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(header)
      writer.writerows(data)



input_filename = "data/fifth_task.html"
output_filename = "task5output.csv"
process_file(input_filename, output_filename)
