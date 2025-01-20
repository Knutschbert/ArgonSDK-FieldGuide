import sqlite3
import csv
import sys
import re

def extract_files(query):
    # Extract tokens ending with .csv from the SQL query
    file_names = re.findall(r'\b(\w+\.csv)\b', query, re.IGNORECASE)
    return file_names

def write_markdown_table(cursor, output_md):
    with open(output_md, 'w', newline='', encoding='utf-8') as mdfile:
        csv_writer = csv.writer(mdfile)
        header = [description[0] for description in cursor.description]
        csv_writer.writerow(header)

        rows = cursor.fetchall()
        for row in rows:
            csv_writer.writerow(row)

        print(f"Markdown table written to {output_md}.")

def create_database(csv_files, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for table, csv_file in csv_files.items():
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            placeholders = ', '.join(['?'] * len(header))

            # Create table
            create_table_query = f'CREATE TABLE {table} ({", ".join(header)})'
            cursor.execute(create_table_query)

            # Insert data into the table
            insert_query = f'INSERT INTO {table} VALUES ({placeholders})'
            cursor.executemany(insert_query, csv_reader)

    conn.commit()
    conn.close()

def execute_query(db_name, query, output_csv):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    # Print the result
    print(result)

    # Write result to CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([description[0] for description in cursor.description])  # Write headers
        csv_writer.writerows(result)
import os
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <sql_query> <output_csv>")
        # sys.exit(1)

    # sql_query = sys.argv[1]
    # output_csv = sys.argv[2]
    sql_query = "SELECT stp2.SourceString as 'Perk Name', stp.SourceString as 'Perk Description' FROM SubclassPerks.csv sp INNER JOIN ST_Class_Perks.csv stp ON sp.Idx || 'Desc' == stp.Key \
        INNER JOIN ST_Class_Perks.csv stp2 ON sp.Idx == stp2.Key"
    # sql_query = "Select sp.Idx FROM SubclassPerks.csv sp"
    
    output_csv = "output.csv"

    # Extract file names from the SQL query
    csv_files = {file_name.split('.')[0] : file_name for file_name in extract_files(sql_query)}

    # Assuming CSV files have the same names as tables but with .csv extension
    create_database(csv_files, 'temp_db.db')
    sql_query = sql_query.replace('.csv','')
    execute_query('temp_db.db', sql_query, output_csv)
    os.remove('temp_db.db')