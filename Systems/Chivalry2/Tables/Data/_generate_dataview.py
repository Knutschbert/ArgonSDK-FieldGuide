import os
import csv

# Function to split a list into chunks of a given size
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Create Tables folder if it doesn't exist
output_folder = os.path.join(os.pardir, "")
os.makedirs(output_folder, exist_ok=True)

# Get the list of CSV files in the current directory
csv_files = [file for file in os.listdir() if file.endswith(".csv")]

# Iterate through each CSV file and create DataTable.md file
for file in csv_files:
    table_name = os.path.splitext(file)[0] + " DataTable.md"
    output_path = os.path.join(output_folder, table_name)
    with open(file, 'r', newline='') as csvfile:
        data = list(csv.reader(csvfile))

        # Get column names from the first row
        columns = data[0]

        # Split the columns into chunks (adjust the chunk size as needed)
        chunk_size = 10  # Number of columns per view
        column_chunks = list(chunk_list(columns, chunk_size))

        # Write Dataview template to DataTable.md file
        with open(output_path, 'w') as output_file:
            # Write links to source files
            output_file.write(f"Source: [{file}]({os.path.abspath(file)})\n\n")

            output_file.write('## Dataview Tables (chunked)\n\n')
            # Write Dataview template for each column chunk
            for idx, chunk in enumerate(column_chunks):
                needsIndex = "Index" in columns and idx != 0
                output_file.write(f'```dataview\n')
                output_file.write(f'TABLE WITHOUT ID {needsIndex and "Idx," or ""}{", ".join(chunk)}\n')
                output_file.write(f'FROM csv("Data/{file}")\n')
                output_file.write(f'```\n\n')

            # Write regular Markdown table with all columns
            output_file.write('## Regular Markdown Table\n\n')
            output_file.write('| ' + ' | '.join(columns) + ' |\n')
            output_file.write('| ' + ' | '.join(['---' for _ in columns]) + ' |\n')
            for row in data[1:]:
                output_file.write('| ' + ' | '.join(row) + ' |\n')

    print(f'Dataview template and regular Markdown table written to {output_path}.')

print('Processing completed.')
