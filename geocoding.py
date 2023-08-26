import googlemaps
import requests

def geocode_address(address, google_api_key):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=google_api_key)
    
    # Geocode the address
    geocode_result = gmaps.geocode(address)
    
    # Extract latitude and longitude
    if geocode_result and len(geocode_result) > 0:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None

def get_neighborhood(latitude, longitude):
    # URL of the reverse geocoding endpoint
    url = "https://www.portlandmaps.com/arcgis/rest/services/Public/COP_OpenData/MapServer/125/query"
    
    # Parameters for the query
    params = {
        "where": f"1=1",
        "geometry": f"{longitude},{latitude}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*",
        "returnGeometry": "false",
        "f": "json"
    }
    
    # Send GET request to the endpoint
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract neighborhood information if available
        if "features" in data and len(data["features"]) > 0:
            attributes = data["features"][0]["attributes"]
            neighborhood = attributes.get("NAME")
            return neighborhood
    return None

def explore_neighborhood_changes(original_address, google_api_key):
    # Get the original neighborhood
    original_latitude, original_longitude = geocode_address(original_address, google_api_key)
    original_neighborhood = get_neighborhood(original_latitude, original_longitude)
    
    # Start exploring neighborhood changes
    address = original_address
    while True:
        latitude, longitude = geocode_address(address, google_api_key)
        if latitude is None or longitude is None:
            print("Geocoding failed.")
            break
        
        current_neighborhood = get_neighborhood(latitude, longitude)
        print("Address:", address)
        print("Neighborhood:", current_neighborhood)
        print("-----------------------------")
        
        if current_neighborhood != original_neighborhood:
            print("Different neighborhood found!")
            print("New Neighborhood:", current_neighborhood)
            print("Address:", address)
            break
        
        address_parts = address.split()
        last_number = int(address_parts[0])
        new_number = last_number + 100
        address = " ".join([str(new_number)] + address_parts[1:])

def main():
    # Google Maps API key
    google_api_key = "REPLACE_WITH_GOOGLE_API"
    
    # Original address to start with
    original_address = "1300 SE Stark Street, Portland, OR 97214"
    
    # Start exploring neighborhood changes
    explore_neighborhood_changes(original_address, google_api_key)

if __name__ == "__main__":
    main()
