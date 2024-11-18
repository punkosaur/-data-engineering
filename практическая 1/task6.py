import requests
import csv

def process_file(output_filename):
    try:
      url = 'https://api.hh.ru/vacancies?text=data&per_page=50'
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()

      vacancies = data.get('items', [])

      csv_data = []
      csv_data.append(["Name", "Company", "Url", "Responsibility"])

      for vacancy in vacancies:
        name = vacancy.get('name', '')
        company = vacancy.get('employer', {}).get('name', '')
        url = vacancy.get('alternate_url', '')
        responsibility = vacancy.get('snippet', {}).get('responsibility', '')
        csv_data.append([name, company, url, responsibility])

      with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

output_filename = "task6output.csv"
process_file(output_filename)

