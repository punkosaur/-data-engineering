import math

def process_file(input_filename, output_filename):

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return

    numbers = []
    for line in lines:
        number = line.strip().split()
        numbers.append(number)

    for line in range(len(numbers)):
        for number in range(len(numbers[line])):
            if numbers[line][number] == 'N/A':
                numbers[line][number] = (numbers[line][number-1] + int(numbers[line][number+1]))/2
            else:
                numbers[line][number] = int(numbers[line][number])

    result = []
    for line in numbers:
        count = 0
        sum = 0.0
        for number in line:
            integer_part = math.floor(number) 
            if number < 0 and number % 2 == 1:
                count += 1
                sum += number
        result.append(sum / count)

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for num in result:
                outfile.write(f"{num}\n")
    except Exception as e:
        print(f"Error writing to file '{output_filename}': {e}")


input_file = 'data/third_task.txt' 
output_file = 'task3output.txt'
process_file(input_file, output_file)