
# Flight Data Query CLI

A Command-Line Interface (CLI) application for querying and displaying flight data from an SQLite database. 
The program allows users to search flights by ID, date, airline, or origin airport while highlighting delayed flights.

## Features
- Retrieve flight details by ID.
- View flights scheduled on a specific date.
- Search delayed flights by airline (case-insensitive, supports partial matches).
- Search delayed flights by origin airport (requires valid IATA code).

## Usage
1. Clone the repository and ensure you have Python installed.
2. Install dependencies (e.g., `sqlalchemy` for database interaction).
3. Run the program:
   ```bash
   python main.py
   ```
4. Use the menu to select options and perform queries.

## Database
- SQLite database located at `data/flights.sqlite3`.

## Requirements
- Python 3.7+
- SQLAlchemy

## Example
```text
Menu:
1. Show flight by ID
2. Show flights by date
3. Delayed flights by airline
4. Delayed flights by origin airport
5. Exit
Enter your choice: 2
Enter date in DD/MM/YYYY format: 25/12/2024
Got 3 results:
1. JFK -> LAX by Delta Airlines, Delay: 45 Minutes
2. ORD -> SFO by United Airlines, Delay: 30 Minutes
3. ATL -> SEA by Southwest Airlines, Delay: 20 Minutes
```
