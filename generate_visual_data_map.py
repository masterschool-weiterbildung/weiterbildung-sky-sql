import folium


def process_data_and_map(origin,
                         destination,
                         origin_lat, origin_long,
                         dest_lat, dest_long,
                         percent_delayed
                         ):
    """
    Creates a Folium map that visualizes the delay percentage for a flight route.

    Parameters:
        origin (str): IATA code of the origin airport.
        destination (str): IATA code of the destination airport.
        origin_lat (str): Latitude of the origin airport.
        origin_long (str): Longitude of the origin airport.
        dest_lat (str): Latitude of the destination airport.
        dest_long (str): Longitude of the destination airport.
        percent_delayed (float): Percentage of delayed flights for the route.

    Output:
        - Saves the map as an HTML file named "flight_delays_map.html".

    Resource:
    https://python-visualization.github.io/folium/latest/user_guide/vector_layers/polyline.html#
    """

    # Create the base map

    m = folium.Map(location=[39.8283, -98.5795],
                   zoom_start=4)  # Centered on the USA

    # Add routes to the map
    folium.PolyLine(
        locations=[
            (float(origin_lat), float(origin_long)),
            (float(dest_lat), float(dest_long))
        ],
        color="green",
        weight=percent_delayed / 5,

        tooltip=f"{origin} <-> {destination} "
                f"({percent_delayed}% delayed)"

    ).add_to(m)

    # Save and display the map
    m.save("flight_delays_map.html")
