url = "https://subway.com.my/find-a-subway"

from langchain_community.document_loaders import AsyncChromiumLoader
from geopy.geocoders import ArcGIS
from sqlalchemy import create_engine


urls = [url]
loader = AsyncChromiumLoader(urls)
docs = loader.load()
content = ""
for doc in docs:
    content += doc.page_content
from bs4 import BeautifulSoup


# Parse the HTML content
soup = BeautifulSoup(content, "html.parser")

location_right = soup.find_all("div", {"class": "location_right"})
location_left = soup.find_all("div", {"class": "location_left"})

data = {
    "name": [],
    "operating_hours": [],
    "address": [],
    "google_maps_link": [],
    "waze_link": [],
    "latitude": [],
    "longitude": [],
}
addresses = []
for left, right in zip(location_left, location_right):
    left_soup = BeautifulSoup(str(left), "html.parser")
    # Extracting address
    address = left_soup.find("div", class_="infoboxcontent").find("p").text.strip()
    address = address.replace(", ", " ").strip()
    if "Kuala Lumpur" in address:
        right_soup = BeautifulSoup(str(right), "html.parser")
        # Find the first <a> tag for Google Maps
        links = right_soup.find_all("a", href=True)
        google_maps_link = links[0]["href"]
        waze_link = links[1]["href"]
        # Extracting name
        name = left_soup.find("h4").text

        # Extracting operating hours
        operating_hours = (
            left_soup.find("div", class_="infoboxcontent").find_all("p")[2].text
        )
        nom = ArcGIS()
        result = nom.geocode(address)
        longitude, latitude = result.longitude, result.latitude
        data["name"].append(name)
        data["operating_hours"].append(operating_hours)
        data["address"].append(address)
        data["google_maps_link"].append(google_maps_link)
        data["waze_link"].append(waze_link)
        data["latitude"].append(latitude)
        data["longitude"].append(longitude)
import pandas as pd

df = pd.DataFrame(data)
# Specify the SQLite database file name
sqlite_db_file = "subway.db"

# Create a SQLite engine
engine = create_engine(f"sqlite:///{sqlite_db_file}")

df.to_sql("subway_table", engine, index=False, if_exists="replace")
