# SQL2DuckDB
This project provides a tool to convert SQL queries written in MySQL syntax to DuckDB-compatible syntax. Leveraging LangChain and Google Gemini Pro, the converter automatically applies DuckDB-specific rules to ensure compatibility, making it ideal for data scientists and engineers transitioning from MySQL to DuckDB.

## Feature
Converts MySQL queries to DuckDB with specific formatting rules trained using the Few Shot Learning Algorithm.

## Prerequisites
Python 3.8+
Google Cloud API Key with access to gemini-pro model
Basic knowledge of MySQL and DuckDB for SQL syntax understanding.

## Setup
1. Clone the repository:
   git clone https://github.com/yourusername/mysql-to-duckdb-converter.git
   cd mysql-to-duckdb-converter
3. Install dependencies:
   pip install -r requirements.txt
5. Environment Variables:
   GOOGLE_API_KEY=your_google_api_key

