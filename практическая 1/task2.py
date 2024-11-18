import math

def process_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return

    sums = []
    for line in lines:
        numbers = [int(x) for x in line.strip().split()]
        line_sum = sum(abs(num) for num in numbers if num**2 < 100000)
        sums.append(line_sum)

    average = sum(sums) / len(sums) if sums else 0

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for i, s in enumerate(sums):
                outfile.write(f"{s}\n")
            outfile.write(f"\n{average:.2f}")
    except Exception as e:
        print(f"Error writing to file '{output_filename}': {e}")


input_file = 'data/second_task.txt' 
output_file = 'task2output.txt'
process_file(input_file, output_file)