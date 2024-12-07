from sqlalchemy import create_engine, text, Sequence, Row
from sqlalchemy.exc import SQLAlchemyError

from util_sql_query import QUERY_FLIGHT_BY_ID, QUERY_FLIGHT_BY_DATE, \
    QUERY_FLIGHT_BY_AIRLINE, QUERY_FLIGHT_BY_ORIGIN_AIRPORT, \
    QUERY_AVG_PERCENTAGE_DELAYED_FLIGHTS, QUERY_LONG_LAT


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """

    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params) -> Sequence[Row]:
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.

        Parameters:
            query (str):
                The SQL query string to execute. This can include placeholders
                for parameters.
            params (dict):
                A dictionary of parameter values to safely inject into the query.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database. Returns an empty
                list if an exception occurs.

        Raises:
                Returns an empty list in case of failure.
        """
        try:
            with self._engine.connect() as connection:
                query = text(query)
                results = connection.execute(query, params)
                return results.fetchall()
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return []

    def get_flight_by_id(self, flight_id) -> Sequence[Row]:
        """
        Retrieve flight details by flight ID.

        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.

        Parameter:
            flight_id (int):
                The unique identifier of the flight to retrieve.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_flights_by_date(self, day, month, year) -> Sequence[Row]:
        """
        Retrieve flights for a specific date with delays.

        Parameters:
            day (int): The day of the flight.
            month (int): The month of the flight.
            year (int): The year of the flight.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.

        Notes:
            - The method uses the `QUERY_FLIGHT_BY_DATE` SQL query.
        """

        params = {'day': day, 'month': month, 'year': year}
        return self._execute_query(QUERY_FLIGHT_BY_DATE, params)

    def get_delayed_flights_by_airline(self, airline: str) -> Sequence[Row]:
        """
        Retrieve delayed flights for a specific airline.

        Parameter:
            airline (str):
                The name (or partial name) of the airline to search for.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.

        Notes:
            - The method uses the `QUERY_FLIGHT_BY_AIRLINE` SQL query.
        """

        params = {'airline': "%" + airline + "%"}
        return self._execute_query(QUERY_FLIGHT_BY_AIRLINE, params)

    def get_delayed_flights_by_airport(self, airport_input: str) -> Sequence[
        Row]:
        """
        Retrieve delayed flights departing from a specific airport.

        Description:
            This method fetches flights departing from a given origin airport
            with departure delays of at least 20 minutes. Results are ordered
            by departure delay in descending order.

        Parameters:
            airport_input (str):
                The IATA code of the origin airport.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.

        Notes:
            - The method uses the `QUERY_FLIGHT_BY_ORIGIN_AIRPORT` SQL query.
        """

        params = {'origin_airport': airport_input}
        return self._execute_query(QUERY_FLIGHT_BY_ORIGIN_AIRPORT, params)

    def generate_percentage_of_delayed_flights(self,
                                               origin_airport: str,
                                               destination_airport: str) -> \
            Sequence[
                Row]:
        """
        Calculates the average percentage of delayed flights between two airports,
        considering both directions: origin to destination and destination to origin.

        Parameters:
            origin_airport (str): The IATA code of the origin airport.
            destination_airport (str): The IATA code of the destination airport.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.
        """
        params = {'origin': origin_airport,
                  'destination': destination_airport,
                  'origin_vv': destination_airport,
                  'destination_vv': origin_airport
                  }
        return self._execute_query(QUERY_AVG_PERCENTAGE_DELAYED_FLIGHTS,
                                   params)

    def get_airport_lat_long(self, origin_airport: str,
                             destination_airport: str) -> Sequence[
        Row]:
        """
        Retrieves the latitude and longitude coordinates for the specified origin
        and destination airports.

        Parameters:
            origin_airport (str): The IATA code of the origin airport.
            destination_airport (str): The IATA code of the destination airport.

        Returns:
            Sequence[Row]:
                A sequence of rows fetched from the database.
        """
        params = {'origin': origin_airport,
                  'destination': destination_airport}

        return self._execute_query(QUERY_LONG_LAT, params)

    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()
