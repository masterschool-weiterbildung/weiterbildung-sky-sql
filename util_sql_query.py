"""
SQL Query Definitions for Flight Data Retrieval.

Description:
    This module contains pre-defined SQL query strings for retrieving flight
    data from a relational database.

Queries:
    QUERY_FLIGHT_BY_ID:
        Retrieves detailed information about a specific flight by its unique ID.

        Parameters:
            - id (int): The unique identifier of the flight.

    QUERY_FLIGHT_BY_DATE:
        Retrieves flights based on a specific date and filters those with
        a departure delay of at least 20 minutes.

        Parameters:
            - day (int): The day of the flight.
            - month (int): The month of the flight.
            - year (int): The year of the flight.

    QUERY_FLIGHT_BY_AIRLINE:
        Retrieves flights for a specific airline, filtering those with a
        departure delay of at least 20 minutes.

        Parameter:
            - airline (str): The name (or partial name) of the airline,
                              case-insensitive.

    QUERY_FLIGHT_BY_ORIGIN_AIRPORT:
        Retrieves flights departing from a specified origin airport and filters
        those with a departure delay of at least 20 minutes.

        Parameter:
            - origin_airport (str): The IATA code of the origin airport.

Notes:
    - The `COALESCE` function ensures null values in `DEPARTURE_DELAY`
      are treated as zero. An empty value should not be treated as a delay.
    - The `DEPARTURE_DELAY` is filtered greater or equal to 20 minutes.
      A flight is considered delayed if it is delayed by 20 minutes or more
"""

QUERY_FLIGHT_BY_ID = ("SELECT flights.*, airlines.airline, flights.ID as "
                      "FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM "
                      "flights JOIN airlines ON flights.airline = airlines.id "
                      "WHERE flights.ID = :id")

QUERY_FLIGHT_BY_DATE = ("SELECT "
                        "   f.id, "
                        "   f.ORIGIN_AIRPORT, "
                        "   f.DESTINATION_AIRPORT, "
                        "   a.AIRLINE, "
                        "   f.DEPARTURE_DELAY AS DELAY "
                        "FROM "
                        "   airlines AS a "
                        "JOIN "
                        "   flights AS f "
                        "ON	a.ID = f.AIRLINE "
                        "WHERE "
                        "   COALESCE(f.DEPARTURE_DELAY, 0) AND "
                        "   f.DAY = :day AND f.MONTH = :month AND f.YEAR = :year "
                        "AND "
                        "   f.DEPARTURE_DELAY >= 20 "
                        "ORDER BY "
                        "DEPARTURE_DELAY DESC "
                        )

QUERY_FLIGHT_BY_AIRLINE = ("SELECT "
                           "   f.id, "
                           "   f.ORIGIN_AIRPORT, "
                           "   f.DESTINATION_AIRPORT, "
                           "   a.AIRLINE, "
                           "   f.DEPARTURE_DELAY AS DELAY "
                           "FROM "
                           "   airlines AS a "
                           "JOIN "
                           "   flights AS f "
                           "ON	a.ID = f.AIRLINE "
                           "WHERE "
                           "   COALESCE(f.DEPARTURE_DELAY, 0) "
                           "AND "
                           "   f.DEPARTURE_DELAY >= 20 "
                           "AND "
                           "   lower(a.AIRLINE) LIKE lower(:airline) "
                           "ORDER BY "
                           "DEPARTURE_DELAY DESC"
                           )

QUERY_FLIGHT_BY_ORIGIN_AIRPORT = ("SELECT "
                                  "   f.id, "
                                  "   f.ORIGIN_AIRPORT, "
                                  "   f.DESTINATION_AIRPORT, "
                                  "   a.AIRLINE, "
                                  "   f.DEPARTURE_DELAY AS DELAY "
                                  "FROM "
                                  "   airlines AS a "
                                  "JOIN "
                                  "   flights AS f "
                                  "ON	a.ID = f.AIRLINE "
                                  "WHERE "
                                  "   COALESCE(f.DEPARTURE_DELAY, 0) "
                                  "AND "
                                  "   f.DEPARTURE_DELAY >= 20 "
                                  "AND "
                                  "   f.ORIGIN_AIRPORT = :origin_airport "
                                  "ORDER BY "
                                  "DEPARTURE_DELAY DESC"
                                  )

QUERY_AVG_PERCENTAGE_DELAYED_FLIGHTS = \
    ("SELECT "
     "   ORIGIN_AIRPORT, "
     "   DESTINATION_AIRPORT, "
     "   AVG(DELAYED_FLIGHTS * 100.0 / TOTAL_FLIGHTS) AS PERCENT_DELAYED "
     "   FROM ( "
     "          SELECT  "
     "          ORIGIN_AIRPORT, "
     "          DESTINATION_AIRPORT, "
     "          COUNT(CASE WHEN DEPARTURE_DELAY >= 20 THEN 0 END) "
     "          AS DELAYED_FLIGHTS, "
     "          COUNT(*) AS TOTAL_FLIGHTS "
     "   FROM flights "
     "   GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT "
     "         ) AS ROUTE_STATS "
     "   WHERE (ORIGIN_AIRPORT = :origin AND DESTINATION_AIRPORT = :destination) "
     "   OR (ORIGIN_AIRPORT = :origin_vv AND DESTINATION_AIRPORT = :destination_vv)"
     "   GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT "
     )

QUERY_LONG_LAT = ("SELECT "
                  "   IATA_CODE, "
                  "   LATITUDE, "
                  "   LONGITUDE "
                  "FROM "
                  "   airports "
                  "WHERE "
                  "   IATA_CODE = :origin "
                  "OR"
                  "   IATA_CODE = :destination "
                  )
