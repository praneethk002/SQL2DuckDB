import os
from dotenv import load_dotenv
from utils import convert_query

# Load environment variables
load_dotenv("config.env")

# Prompt the user to enter a multi-line MySQL query
print("Please enter the MySQL query to be converted to DuckDB format (press Enter twice to finish):")

# Collect multi-line input until an empty line is entered
query_input_lines = []
while True:
    line = input()
    if line == "":
        break
    query_input_lines.append(line)

# Join the lines to form the full query
query_input = "\n".join(query_input_lines)

# Convert and print the formatted DuckDB query
cleaned_query = convert_query(query_input)
print("\nFormatted DuckDB Query:\n", cleaned_query)
