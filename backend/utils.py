from geopy.distance import geodesic


def filter_branches_within_radius(
    selected_station_data, all_data, selected_station, radius=5
):
    branches_within_radius = []

    for _, row in all_data.iterrows():
        branch_location = (row["latitude"], row["longitude"])
        distance = geodesic(selected_station_data, branch_location).kilometers
        if distance <= radius and row["name"] != selected_station:
            branches_within_radius.append(row.to_dict())

    return branches_within_radius
