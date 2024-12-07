import data
from datetime import datetime
import sqlalchemy

from generate_visual_data_map import process_data_and_map

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3


def generate_percentage_of_delayed_flights(data_manager) -> None:
    """
    Prompts the user to input origin and destination airport IATA codes,
    calculates the average percentage of delayed flights between them, and
    visualizes the result on a map.

    Parameter:
        data_manager: An instance of the FlightData class that provides access
                      to flight-related queries.
    """
    global airport_origin_input, airport_destination_input
    valid = False
    while not valid:
        airport_origin_input = input("Enter origin airport IATA code: ")
        airport_destination_input = input(
            "Enter destination airport IATA code: ")

        if (airport_origin_input.isalpha()
                and len(airport_origin_input) == IATA_LENGTH
                and airport_destination_input.isalpha()
                and len(airport_destination_input) == IATA_LENGTH):
            valid = True

    results_percent_delayed = (
        data_manager.generate_percentage_of_delayed_flights
        (airport_origin_input, airport_destination_input))

    results_percent_delayed = (results_percent_delayed[0][2] +
                               results_percent_delayed[1][2]) / 2

    results_lat_long = (data_manager.get_airport_lat_long
                        (airport_origin_input, airport_destination_input))

    process_data_and_map(airport_origin_input,
                         airport_destination_input,
                         results_lat_long[0][1],
                         results_lat_long[0][2],
                         results_lat_long[1][1],
                         results_lat_long[1][2],
                         results_percent_delayed
                         )
    print(
        f"Origin: {airport_origin_input} <-> Destination: "
        f"{airport_destination_input} ({results_percent_delayed}% delayed)")


def delayed_flights_by_airline(data_manager) -> None:
    """
    Retrieve and display delayed flights for a specific airline.

    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.

    Parameters:
        data_manager (FlightData):
            The data manager instance for executing database queries.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager) -> None:
    """
    Retrieve and display delayed flights for a specific origin airport.

    Asks the user for a textual IATA 3-letter airport code (loops until input
    is valid). Then runs the query using the data object method
    "get_delayed_flights_by_airport". When results are back, calls
    "print_results" to show them to on the screen.

    Parameters:
        data_manager (FlightData):
            The data manager instance for executing database queries.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Valide input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager) -> None:
    """
    Retrieve and display flight details by flight ID.

    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.

    Parameters:
    data_manager (FlightData):
        The data manager instance for executing database queries.

    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager) -> None:
    """
    Retrieve and display flights for a specific date.
    Prompts the user to input a date in the format 'DD/MM/YYYY'

    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.

    Parameters:
    data_manager (FlightData):
        The data manager instance for executing database queries.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again... [DD/MM/YYYY] ", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month,
                                               date.year)
    print_results(results)


def print_results(results) -> None:
    """
    Display query results in a readable format.

    Get a list of flight results (List of dictionary-like objects from
    SQLAachemy). Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.

    Parameters:
        results (list of RowProxy):
            A list of dictionary-like objects containing flight details.
            Each object must include the columns: `ID`, `ORIGIN_AIRPORT`,
            `DESTINATION_AIRPORT`, `AIRLINE`, and `DELAY`.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        # turn result into dictionary
        result = result._mapping

        # Check that all required columns are in place
        try:
            delay = int(result['DELAY']) if result[
                'DELAY'] else 0  # If delay columns is NULL, set it to 0
            origin = result['ORIGIN_AIRPORT']
            dest = result['DESTINATION_AIRPORT']
            airline = result['AIRLINE']
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(
                f"{result['ID']}. {origin} -> {dest} by {airline}, "
                f"Delay: {delay} Minutes")
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    """
    Display the menu and get the user's choice.

    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.

    Returns:
            A function pointer corresponding to the user's choice.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input("Enter choice: "))
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("Try again...")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = {1: (flight_by_id, "Show flight by ID"),
             2: (flights_by_date, "Show flights by date"),
             3: (delayed_flights_by_airline, "Delayed flights by airline"),
             4: (
                 delayed_flights_by_airport,
                 "Delayed flights by origin airport"),
             5: (
                 generate_percentage_of_delayed_flights,
                 "Generate Visual Map for delayed flights"),
             6: (quit, "Exit")
             }


def main():
    # Main program entry point.

    # Create an instance of the Data Object using our SQLite URI
    data_manager = data.FlightData(SQLITE_URI)

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
