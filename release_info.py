from dataclasses import dataclass, field
from typing import List, Optional
import pyperclip
import requests
import json
# Assuming TrackInfo is defined elsewhere (e.g., import it if needed)

DISCOGS_URL = "https://api.discogs.com/database/search"
DISCOGS_RELEASE_URL = "https://api.discogs.com/releases/"
DISCOGS_HEADERS = {
    "User-Agent": "MyVinylLookupApp/1.0",
    "Authorization": "Discogs token=xZuxPGRhgXGrvRStDnPHiZmXxynpadsxPxbwseph"
}

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/release"
DISCOGS_RELEASE_URL = "https://api.discogs.com/releases/"
MUSICBRAINZ_HEADERS = {
    "User-Agent": "cd_scanner/1.0 (scottnichol67@icloud.com)"
}

@dataclass
class TrackInfo:
    position: str = 'Unknown'
    title: str = 'Unknown'
    duration: str = 'Unknown'

    def __str__(self):
        return f"{self.position}. {self.title} ({self.duration_in_minutes_seconds()})"
    
    def duration_in_minutes_seconds(self):
        if self.duration == 'Unknown':
            return 'Unknown'
        try:
            total_seconds = int(self.duration) // 1000
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}:{str(seconds).zfill(2)}"
        except ValueError:
            return 'Unknown'

@dataclass
class ReleaseInfo:
    id: str = 'Unknown'
    artist: str = 'Unknown'
    title: str = 'Unknown'
    year: str = 'Unknown'
    label: str = 'Unknown'
    catalog_number: str = 'Unknown'
    country: str = 'Unknown'
    packaging: str = 'Unknown'
    media_format: str = 'Unknown'
    barcode: str = 'Unknown'
    url: str = 'Unknown'
    source: str = 'Unknown'
    tracks: Optional[List[TrackInfo]] = None  # Fixed: Proper type hint allowing None

    def __str__(self):
        return f"\"{self.id}\",\"{self.artist}\",\"{self.title}\",\"{self.year}\",\"{self.media_format}\",\"{self.packaging}\",\"{self.label}\",\"{self.catalog_number}\",\"{self.country}\",\"{self.barcode}\",\"{self.url}\",\"{self.source}\""
    def copy_to_clipboard(self):
        pyperclip.copy(str(self))
        print("Release information copied to clipboard!")
    def print_info(self):
        print(f"{self.title} Details:")
        print(f"  ID: {self.id}")
        print(f"  Artist: {self.artist}")
        print(f"  Title: {self.title}")
        print(f"  Year: {self.year}")
        print(f"  Label: {self.label}")
        print(f"  Catalog Number: {self.catalog_number}")
        print(f"  Country: {self.country}")
        print(f"  Format: {self.media_format}")
        print(f"  Packaging: {self.packaging}")
        print(f"  Barcode: {self.barcode}")
        print(f"  URL: {self.url}")
        print(f"  Source: {self.source}")

        if (self.tracks):
            print("  Tracklist:")
            for track in self.tracks:
                print(f"    {track}")
    
    def init_with_discogs_data(self, data):
        self.id = str(data.get('id', 'Unknown'))
        self.artist = data.get('artists_sort', 'Unknown')
        self.title = data.get('title', 'Unknown')
        self.year = data.get('year', 'Unknown')

        labels = data.get('labels', [])
        self.label = labels[0].get('name', 'Unknown') if labels else 'Unknown'
        self.catalog_number = labels[0].get('catno', 'Unknown') if labels else 'Unknown'
        
        self.country = data.get('country', 'Unknown')

        formats = data.get('formats', [])
        self.packaging = formats[0].get('text', 'Unknown') if formats else 'Unknown'
        self.media_format = formats[0].get('name', 'Unknown') if formats else 'Unknown'

        identifiers = data.get('identifiers', [])
        self.barcode = next((id.get('value') for id in identifiers if id.get('type') == 'Barcode'), 'Unknown')
        self.url = data.get('uri', 'Unknown')
        self.source = "Discogs"

    def init_with_musicbrainz_data(self, data):
        self.id = str(data.get('id', 'Unknown'))
        self.artist = data.get('artist-credit', [{}])[0].get('artist', {}).get('name', 'Unknown')
        self.title = data.get('title', 'Unknown')
        self.year = data.get('date', 'Unknown')[:4] if data.get('date') else 'Unknown'
        
        label_info = data.get('label-info', [{}])[0]
        self.label = label_info.get('label', {}).get('name', 'Unknown') if label_info else 'Unknown'
        self.catalog_number = label_info.get('catalog-number', 'Unknown') if label_info else 'Unknown'
        
        self.country = data.get('country', 'Unknown')
        self.packaging = data.get('packaging', 'Unknown')
        self.media_format = data.get('media', [{}])[0].get('format', 'Unknown') if data.get('media') else 'Unknown'
        self.barcode = data.get('barcode', 'Unknown')
        self.url = f"https://musicbrainz.org/release/{self.id}" if self.id != 'Unknown' else 'Unknown'
        self.source = "MusicBrainz"

    def get_discogs_by_id(self, id):
        url = f"{DISCOGS_RELEASE_URL}{id}"
        response = requests.get(url, headers=DISCOGS_HEADERS)
        response.raise_for_status()
        return response.json()

    def search_discogs_by_catno(self, catno, format_filter="Vinyl"):
        params = {
            "catno": catno,
            "format": format_filter,
            "type": "release",
            "per_page": 10
        }
        response = requests.get(DISCOGS_URL, headers=DISCOGS_HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    def search_discogs_by_artist_and_title(self, artist, title, format_filter="Vinyl"):
        params = {
            "artist": artist,
            "title": title,
            "format": format_filter,
            "type": "release",
            "per_page": 10
        }
        response = requests.get(DISCOGS_URL, headers=DISCOGS_HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    def search_discogs_by_barcode(self, barcode, format_filter="Vinyl"):
        params = {
            "barcode": barcode,
            "format": format_filter,
            "type": "release",
            "per_page": 10
        }
        response = requests.get(DISCOGS_URL, headers=DISCOGS_HEADERS, params=params)
        response.raise_for_status()
        return response.json()

    def find_release_on_discogs(self, key):
        """
        Find a release by catalog number using the Discogs API.
        
        Args:
            key (str): The catalog number or barcode of the release
            
        Returns:
            dict: Release information if found, None otherwise
        """
        data = None

        # First check if the key is a barcode (12 or 13 digit number)
        if key.isdigit() and len(key) in [12, 13]:  # Likely a barcode
            print(f"Searching Discogs for release with barcode: {key}")
            data = self.search_discogs_by_barcode(key)
        
        # If not found by barcode, check if it's in the format "Artist: Title"
        if ':' in key: 
            parts = key.split(':', 1)
            artist = parts[0].strip()
            title = parts[1].strip()
            print(f"Searching Discogs for release with artist: '{artist}' and title: '{title}'")
            data = self.search_discogs_by_artist_and_title(artist, title)
        
        # If still not found, assume it's a catalog number
        if not data:
            print(f"Searching Discogs for release with catalog number: {key}")
            data = self.search_discogs_by_catno(key)
        
        relsease = None
        # If we got results, return the first one (or prompt user if multiple)
        if (data and data.get("results")):
            releases = data.get("results", [])

            # If there's only one release, use it. Otherwise, prompt the user to select from the list.
            if releases and len(releases) == 1:
                release = releases[0]

            elif releases and len(releases) > 1:
                print(f"Multiple releases found for '{key}':")
                for idx, rel in enumerate(releases):
                    # print(json.dumps(rel, indent=2))  # Print raw master data for debugging
                    label = rel.get('label', [{}])[0] if rel.get('label') else None
                    catalog_number = rel.get('catno', 'Unknown')
                    
                    print(f"{idx + 1}. {rel.get('title', 'Unknown')} ({rel.get('year', 'Unknown')}) - {rel.get('country', 'Unknown')} - {rel.get('format', 'Unknown')} - {rel.get('formats', [{}])[0].get('text', 'Unknown')} - Label: {label}, Catalog Number: {catalog_number}")
                selection = input("Enter the number of the correct release (or '0' to skip): ").strip()
                
                # Validate user input and select the release
                if selection.isdigit() and 1 <= int(selection) <= len(releases):
                    release = releases[int(selection) - 1]
                else:
                    release = None
                    print("Skipping this entry.")

        # If we found a release, get the full details and initialize the record
        if release:
            print(json.dumps(release, indent=2))  # Print raw master data for debugging
            record = self.get_discogs_by_id(release.get("id"))
            self.init_with_discogs_data(record)
            self.print_info()
            self.copy_to_clipboard()


        return release

    def search_mbz_by_upc(self, upc):
        """
        Find a CD release by its UPC code using the MusicBrainz API.
        
        Args:
            upc (str): The UPC code of the CD
            
        Returns:
            dict: Release information if found, None otherwise
        """
        params = {
            "query": f"barcode:{upc}",
            "fmt": "json"
        }
        
        try:
            pr = requests.PreparedRequest()
            pr.prepare_url(MUSICBRAINZ_URL, params)
            print(f"Requesting URL: {pr.url}")
            response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("releases") and len(data["releases"]) > 0:
                return data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error querying MusicBrainz: {e}")
            return None

    def search_mbz_by_catno(self, catno):
        """
        Find a release by its catalog number using the MusicBrainz API.
        
        Args:
            catno (str): The catalog number of the release
            
        Returns:
            dict: Release information if found, None otherwise
        """    
        params = {
            "query": f"catno:{catno}",
            "fmt": "json"
        }
        
        try:
            pr = requests.PreparedRequest()
            pr.prepare_url(MUSICBRAINZ_URL, params)
            print(f"Requesting URL: {pr.url}")
            response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("releases") and len(data["releases"]) > 0:
                return data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error querying MusicBrainz: {e}")
            return None

    def search_mbz_by_artist_and_title(self, artist, title):

        """
        Find a release by artist and title using the MusicBrainz API.
        
        Args:
            artist (str): The name of the artist
            title (str): The title of the release
        Returns:
            dict: Release information if found, None otherwise
        """
        print(f"Searching for release with artist: '{artist}' and title: '{title}'")
        params = {
            "query": f"artist:{artist} AND title:{title}",
            "fmt": "json"
        }
        
        try:
            pr = requests.PreparedRequest()
            pr.prepare_url(MUSICBRAINZ_URL, params)
            print(f"Requesting URL: {pr.url}")
            response = requests.get(MUSICBRAINZ_URL, headers=MUSICBRAINZ_HEADERS, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("releases") and len(data["releases"]) > 0:
                return data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error querying MusicBrainz: {e}")
            return None

    def find_release_on_mbz(self, key):
        """
        Find a release by either UPC code or catalog number.
        
        Args:
            key (str): The UPC code or catalog number of the release
            
        Returns:
            dict: Release information if found, None otherwise
        """
        
        data = None
        # First check if the key is a UPC code (12 or 13 digit number)
        if key.isdigit() and len(key) in [12, 13]:
            print(f"Searching for release with UPC code: {key}")
            data = self.search_mbz_by_upc(key)
            if data:
                return data
    
        # If the key contains a colon, assume it's in the format "Artist: Title"
        if ':' in key:
            print(f"Searching for release with Artist and Title: {key}")
            parts = key.split(':', 1)
            artist = parts[0].strip()
            title = parts[1].strip()
            data = self.search_mbz_by_artist_and_title(artist, title)

        # If not found by UPC or artist/title, assume it's a catalog number
        if not data:
            print(f"Searching for release with catalog number: {key}")
            data = self.search_mbz_by_catno(key)

        release = None
        # If we got results, return the first one (or prompt user if multiple)
        if data and data.get("releases") and len(data["releases"]) > 0:
            if len(data["releases"]) == 1:
                release = data["releases"][0]
            else:
                print(f"Multiple releases found for '{key}':")
                for idx, rel in enumerate(data["releases"]):
                    # print(json.dumps(rel, indent=2))  # Print raw master data for debugging
                    format = rel.get('media', [{}])[0].get('format', 'Unknown') if rel.get('media') else 'Unknown'
                    print(f"{idx + 1}. {rel.get('title', 'Unknown')} by {rel.get('artist-credit', [{}])[0].get('artist', {}).get('name', 'Unknown')} {rel.get('date', 'Unknown')} {rel.get('country', 'Unknown')} {format} {rel.get('label-info', 'Unknown')}")
                selection = input("Enter the number of the correct release (or 'q' to skip): ").strip()
                if selection.lower() == 'q':
                    print("Skipping this release.")
                    release = None
                try:
                    selected_index = int(selection) - 1
                    if 0 <= selected_index < len(data["releases"]):
                        release = data["releases"][selected_index]
                    else:
                        print("Invalid selection. Skipping this release.")
                        release = None
                except ValueError:
                    print("Invalid input. Skipping this release.")
                    release = None
        
        # If we found a release, initialize the record
        if(release):
            self.init_with_musicbrainz_data(release)
            self.print_info()
            self.copy_to_clipboard()

        return release
    
    def get_tracklist_from_mbz(self, release_id):
        """
        Get the tracklist for a release from MusicBrainz.
        
        Args:
            release_id (str): The MusicBrainz ID of the release
        Returns:
            list: A list of TrackInfo objects representing the tracklist
        """
        url = f"{MUSICBRAINZ_URL}/{release_id}"
        params = {
            "inc": "recordings",
            "fmt": "json"
        }
        
        try:
            pr = requests.PreparedRequest()
            pr.prepare_url(url, params)
            print(f"Requesting URL: {pr.url}")
            response = requests.get(url, headers=MUSICBRAINZ_HEADERS, params=params)
            response.raise_for_status()
            
            data = response.json()
            tracklist = []
            for medium in data.get("media", []):
                for track in medium.get("tracks", []):
                    track_info = TrackInfo(
                        position=track.get("position", "Unknown"),
                        title=track.get("title", "Unknown"),
                        duration=track.get("length", "Unknown")
                    )
                    tracklist.append(track_info)
            self.tracks = tracklist  # Store the tracklist in the ReleaseInfo object
            return tracklist
        
        except requests.exceptions.RequestException as e:
            print(f"Error querying MusicBrainz for tracklist: {e}")
            return []
