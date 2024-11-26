import numpy as np
import os

def shrek(input_filename, output_filename):

  try:
    matrix = np.load(input_filename)
  except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    return None

  x, y, z = [], [], []

  rows, cols = matrix.shape

  for i in range(rows):
    for j in range(cols):
      if (matrix[i][j] > 510): # 500+10 вариант
        x.append(i)
        y.append(j)
        x.append(matrix[i, j])
  
  x = np.array(x)
  y = np.array(y)
  z = np.array(z)

  np.savez(output_filename, x=x, y=y, z=z)
  np.savez_compressed(output_filename.replace(".npz", "_compressed.npz"), x=x, y=y, z=z)# сжатие

  uncompressed_size = os.path.getsize(output_filename)
  compressed_size = os.path.getsize(output_filename.replace(".npz", "_compressed.npz"))

  print(f"Размер несжатого файла: {uncompressed_size} байт")
  print(f"Размер сжатого файла: {compressed_size} байт")
  print(f"Несжатый больше сжатого в {uncompressed_size / compressed_size:.2f} раз(а)")


input_file = "data/second_task.npy"
output_file = 'task2output.npz'
results = shrek(input_file, output_file)


