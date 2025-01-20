import os
import csv

# Get the list of CSV files in the current directory
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

# Iterate through each CSV file and modify the "---" column
for file in csv_files:
    with open(file, 'r', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        
        # Check if the first column header is "---"
        if data and data[0][0] == '---':
            # Replace "---" with "Index"
            data[0][0] = 'Index'

            # Write the modified data back to the CSV file
            with open(file, 'w', newline='') as csvfile:
                csv.writer(csvfile).writerows(data)

            print(f'Replaced "---" column in {file} with "Index".')
        else:
            print(f'No modification needed in {file}.')

print('Processing completed.')