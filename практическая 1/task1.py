import re
from collections import Counter

def count_word_frequencies(input_filename, output_filename):
  try:
    with open(input_filename, 'r', encoding='utf-8') as infile:
      text = infile.read()
  except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    return

  text = re.sub(r'[^\w\s]', '', text).lower() 
  words = text.split()
  word_counts = Counter(words)
  sorted_word_counts = word_counts.most_common()

  try:
    with open(output_filename, 'w', encoding='utf-8') as outfile:
      for word, count in sorted_word_counts:
        outfile.write(f"{word}:{count}\n")
  except Exception as e:
    print(f"Error writing to output file: {e}")

def analyze_text(input_filename, output_filename):

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            text = infile.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_filename} не найден.")
        return

    paragraphs = re.split(r'\n\n+', text)

    sentence_counts = []
    for paragraph in paragraphs:
        sentences = re.split(r'[.!?]\s', paragraph)
        sentence_counts.append(len(sentences))

    if not sentence_counts:
        average_sentences = 0
    else:
        average_sentences = sum(sentence_counts) / len(sentence_counts)

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(f"{average_sentences:.2f}")
    except Exception as e:
        print(f"Ошибка при записи в файл {output_filename}: {e}")


input_file = 'data/first_task.txt' 
output_file = 'task1output.txt'
outputvar_file = 'task1outputvar10.txt'
count_word_frequencies(input_file, output_file) 
analyze_text(input_file, outputvar_file) 