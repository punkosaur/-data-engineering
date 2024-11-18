import pandas as pd

def process_csv(input_filename, output_summary_filename, output_modified_filename):
    try:
        df = pd.read_csv(input_filename)

        if 'expiration_date' in df.columns:
            df = df.drop(columns=['expiration_date'])

        if 'rating' in df.columns:
            average_rating = df['rating'].mean()

        max_rating = df['rating'].max()

        min_rating = df['rating'].min()

        if 'price' in df.columns:
            filtered_df = df[df['price'] < 9425]
            filtered_df.to_csv(output_modified_filename, index=False)

        with open(output_summary_filename, 'w') as f:
            f.write(f"{average_rating}\n")
            f.write(f"{max_rating}\n")
            f.write(f"{min_rating}\n")


    except Exception as e:
        print(f"An unexpected error occurred: {e}")


input_file = "data/fourth_task.txt"  
outputvar_file = 'task4outputvar10.txt'
output_file = 'task4output.csv'

process_csv(input_file, outputvar_file, output_file)


