import streamlit as st
import folium
import requests
from streamlit_folium import st_folium


def interface_display():
    if ("first_time" not in st.session_state) or ("names" not in st.session_state):
        st.session_state.first_time = True
        st.session_state.names = []
    if st.session_state.first_time:
        names = requests.get("http://127.0.0.1:8000/get_branches").json()["names"]
        st.session_state.names = names

    selected_station = st.selectbox("Select a subway station", st.session_state.names)

    st.markdown(
        "Green Color Locations are those branches within 5km of selected branch"
    )
    params = {"selected_station": str(selected_station)}

    results = requests.post(
        "http://127.0.0.1:8000/get_data",
        params=params,
    ).json()

    m = folium.Map(
        location=list(results["branch_location"]),
        zoom_start=13,
    )

    # Create markers for selected station and branches within 5 km
    fg = folium.FeatureGroup(name="Branches within 5 km")

    # Marker for selected station (usual color)
    fg.add_child(
        folium.Marker(
            location=list(results["branch_location"]),
            popup=selected_station,
            tooltip=selected_station,
        )
    )

    # Markers for branches within 5 km (green color)
    for branch in results["branches_within_radius"]:
        fg.add_child(
            folium.Marker(
                location=[branch["latitude"], branch["longitude"]],
                popup=branch["name"],
                tooltip=branch["name"],
                icon=(folium.Icon(color="green")),
            )
        )

    st_folium(
        m,
        feature_group_to_add=fg,
        width=800,
        height=500,
        center=results["branch_location"],
    )
    # Add an input field
    query = st.text_input("Enter a query:")

    if st.button("Send Message") and query:
        with st.spinner("Waiting for response ..."):
            params = {"query": query}
            response = requests.post(
                "http://127.0.0.1:8000/response",
                params=params,
            ).json()
            display_text = response["response"]
            # Display response based on the input query
            st.markdown(display_text)


if __name__ == "__main__":
    interface_display()
