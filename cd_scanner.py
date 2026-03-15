import json
import os
import pyperclip
import requests
import release_info

# MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release"
# DISCOGS_RELEASE_URL = "https://api.discogs.com/releases/"
# MUSICBRAINZ_HEADERS = {
#     "User-Agent": "cd_scanner/1.0 (scottnichol67@icloud.com)"
# }

# def find_cd_by_upc(upc):
#     """
#     Find a CD release by its UPC code using the MusicBrainz API.
    
#     Args:
#         upc (str): The UPC code of the CD
        
#     Returns:
#         dict: Release information if found, None otherwise
#     """
#     params = {
#         "query": f"barcode:{upc}",
#         "fmt": "json"
#     }
    
#     try:
#         pr = requests.PreparedRequest()
#         pr.prepare_url(MUSICBRAINZ_URL, params)
#         print(f"Requesting URL: {pr.url}")
#         response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
#         response.raise_for_status()
        
#         data = response.json()
        
#         if data.get("releases") and len(data["releases"]) > 0:
#             return data
#         else:
#             return None
            
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying MusicBrainz: {e}")
#         return None

# def find_by_catno(catno):
#     """
#     Find a release by its catalog number using the MusicBrainz API.
    
#     Args:
#         catno (str): The catalog number of the release
        
#     Returns:
#         dict: Release information if found, None otherwise
#     """    
#     params = {
#         "query": f"catno:{catno}",
#         "fmt": "json"
#     }
    
#     try:
#         pr = requests.PreparedRequest()
#         pr.prepare_url(MUSICBRAINZ_URL, params)
#         print(f"Requesting URL: {pr.url}")
#         response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
#         response.raise_for_status()
        
#         data = response.json()
        
#         if data.get("releases") and len(data["releases"]) > 0:
#             return data
#         else:
#             return None
            
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying MusicBrainz: {e}")
#         return None

# def find_by_artist_and_title(artist, title):

#     """
#     Find a release by artist and title using the MusicBrainz API.
    
#     Args:
#         artist (str): The name of the artist
#         title (str): The title of the release
#     Returns:
#         dict: Release information if found, None otherwise
#     """
#     params = {
#         "query": f"artist:{artist} AND title:{title}",
#         "fmt": "json"
#     }
    
#     try:
#         pr = requests.PreparedRequest()
#         pr.prepare_url(MUSICBRAINZ_URL, params)
#         print(f"Requesting URL: {pr.url}")
#         response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
#         response.raise_for_status()
        
#         data = response.json()
        
#         if data.get("releases") and len(data["releases"]) > 0:
#             return data
#         else:
#             return None
            
#     except requests.exceptions.RequestException as e:
#         print(f"Error querying MusicBrainz: {e}")
#         return None

# def find_release(key):
#     """
#     Find a release by either UPC code or catalog number.
    
#     Args:
#         key (str): The UPC code or catalog number of the release
        
#     Returns:
#         dict: Release information if found, None otherwise
#     """
    
#     data = None

#     if key.isdigit() and len(key) in [12, 13]:  # Likely a UPC code
#         print(f"Searching for release with UPC code: {key}")
#         data = find_cd_by_upc(key)
#         if data:
#             return data
   
#     if ':' in key: # Assume it's in the format "Artist: Title"
#         parts = key.split(':', 1)
#         artist = parts[0].strip()
#         title = parts[1].strip()
#         print(f"Searching for release with artist: '{artist}' and title: '{title}'")
#         data = find_by_artist_and_title(artist, title)
#         if data:
#             return data

#     if not data:  # Assume it's a catalog number
#         print(f"Searching for release with catalog number: {key}")
#         data = find_by_catno(key)
#         if data:
#             return data
        
#     return None

if __name__ == "__main__":
    # Initialize catalog.csv with header if it doesn't exist
    if not os.path.exists('catalog_cd.csv'):
        with open('catalog_cd.csv', 'w', encoding='utf-8', newline='') as f:
            f.write("ID,Artist,Title,Year,Format,Packaging,Label,Catalog Number,Country,Barcode,URL,Source\n")
        print("Created catalog_cd.csv with header row.")

    while True:
        upc_code = input("Enter CD UPC code, catalog number, or Artist:Title (or 'q' to quit): ").strip()
        if upc_code.lower() == 'q':
            print("Exiting.")
            break
        
        master_record = release_info.ReleaseInfo()
        release = None

        release = master_record.find_release_on_mbz(upc_code)
        if(release):
            csvline = str(master_record)
            # Append the CSV line to catalog.csv
            try:
                with open('catalog_cd.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write(csvline + '\n')
                print("Appended release to catalog_cd.csv")
            except Exception as e:
                print(f"Failed to append to catalog_cd.csv: {e}")

        else:
            print(f"No release found for UPC code or catalog number: {upc_code}")

            import requests

