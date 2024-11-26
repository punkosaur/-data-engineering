import numpy as np
import json

def shrek(input_filename, output_filename, json_file):

  try:
    matrix = np.load(input_filename)
  except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    return


  sum_all = np.sum(matrix)
  avg_all = np.mean(matrix)

  md = np.diag(matrix)
  sum_md = np.sum(md)
  avg_md = np.mean(md)

  sd = np.diag(np.fliplr(matrix))
  sum_sd = np.sum(sd)
  avg_sd = np.mean(sd)

  max_val = np.max(matrix)
  min_val = np.min(matrix)

  normalized_matrix = (matrix - min_val) / (max_val - min_val)
  np.save(output_filename, normalized_matrix)

  results = {
    "sum": float(sum_all),
    "avr": float(avg_all),
    "sumMD": float(sum_md),
    "avrMD": float(avg_md),
    "sumSD": float(sum_sd),
    "avrSD": float(avg_sd),
    "max": float(max_val),
    "min": float(min_val),
  }

  with open(json_file, 'w', encoding='utf-8') as json_out:
    json.dump(results, json_out, indent=0)


input_file = "data/first_task.npy" 
output_file = 'task1output.npy'
json_file = 'task1output_json.json'
results = shrek(input_file, output_file, json_file)


