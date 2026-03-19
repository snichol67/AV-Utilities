#!/usr/bin/env python3
import subprocess
import json
import sys
import requests
import release_info
from pathlib import Path


if (len(sys.argv) < 3):
    print("usage: audio_excavator input_file output_directory chapters_file [artist] [album] [year]")
    sys.exit(1)

def lookup_tracklist(artist, album):
    if (len(artist) == 0 or len(album) == 0):
        return []
    
    print(f"Looking up tracklist from MusicBrainz for {artist} / {album}...")
    headers = {'User-Agent': 'AudioExcavator/0.1a (scottnichol67@icloud.com)'}
    q = f'release:"{album}" AND artist:"{artist}"'

    print(f"Query: {q}")
    
    r = requests.get('https://musicbrainz.org/ws/2/release/', params={'query': q, 'fmt': 'json'}, headers=headers)

    print("URL:", r.url)

    count = r.json().get('count', 0)
    if count == 0:
        print("No releases found on MusicBrainz.")
        return []

    mbid = r.json()['releases'][0]['id']
    # result = r.json()
    # print("Result: ", result)

    r2 = requests.get(f'https://musicbrainz.org/ws/2/release/{mbid}',
                    params={'fmt': 'json', 'inc': 'recordings'}, headers=headers)
    tracks = [t['title'] for m in r2.json().get('media', []) for t in m.get('tracks', [])]
    return tracks

input_file = sys.argv[1]
output_folder = sys.argv[2]
artist = "" if len(sys.argv) < 4 else sys.argv[3].replace('"', '').replace("'", "")
album = "" if len(sys.argv) < 5 else sys.argv[4].replace('"', '').replace("'", "")

# Create output directory if it doesn't exist
Path(output_folder).mkdir(parents=True, exist_ok=True)

try:
    # Get chapters using ffprobe

    cmd = ['ffprobe', '-v', 'error', '-print_format', 'json', '-show_chapters', input_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    data = json.loads(output)
    chapters = data["chapters"]
except Exception as e:
    print(f"Failed to get chapters from file: {e}")
    sys.exit(1)

print(f"Total chapters: {len(chapters)}")
print(f"Input File: {input_file}")
print(f"Artist: {artist}")
print(f"Album: {album}")
search_key = f"{artist}:{album}" if (len(artist) > 0 and len(album) > 0) else ""
print(f"Search Key: {search_key}")

release_info = release_info.ReleaseInfo()
release = None
if len(search_key) > 0:
    release = release_info.find_release_on_mbz(search_key)
    release_id = release.get("id", "N/A") if release else "N/A"
    print(f"Found release with ID: {release_id}")
    release_info.get_tracklist_from_mbz(release_id)
    release_info.print_info()

    # print(json.dumps(release, indent=2))
    ok = input("Are these titles good? Y/N: ")

titles = [None] * len(chapters)

# If the user accepts the MusicBrainz titles, use them; otherwise, prompt for manual entry
if ok.strip().lower() == 'y' and len(release_info.tracks) >= len(chapters):
    j = 0
    for j in range(len(chapters)):
        titles[j] = release_info.tracks[j].title
        j = j + 1
else:
    j = 0
    for chapter in chapters:
        title = chapter["tags"]["title"]
        user_input = input(f"Enter Song Title for {title} (or press Enter to keep): ")

        if user_input.strip() != "":
            titles[j] = user_input
        else:
            titles[j] = title
        j = j + 1

    for title in titles:
        print(f"Track {j} Title: {title}")
        j = j + 1

    ok = input("Are the titles good? Y/N: ")

if ok.strip().lower() == 'y':
    i = 1
    for chapter in chapters:
        start_time = chapter["start_time"]
        end_time = chapter["end_time"]
        title = titles[i-1]
        song_name = title.replace(" ", "-").replace("\\", "-").replace("/", "-").replace(".", "").replace(":", "-").replace(";", "-").replace("*", "").replace("^", "-").replace("%", "-").replace("$", "-").replace("#", "-").replace("!", "-").replace("`", "").replace("~", "-").replace(",", "-").replace("?", "-")
        output_file = output_folder + '/' + str(i).zfill(2) + '-' + song_name + '.flac'
        track_meta = 'track=' + str(i) 

        # print(f"Title: {title}\nStart Time: {start_time}\nEnd Time: {end_time}\nOutput File: {output_file} {metadata_album} {metadata_artist} {metadata_year}\n")
        encode_cmd = ['ffmpeg', '-hide_banner', '-v', 'error', '-i', input_file, '-ss', start_time, '-to', end_time, '-map', '0:a:0', '-vn', '-c:a', 'flac', '-metadata', track_meta, '-y', output_file]

        if (len(release_info.title) > 0 and release_info.title != "Unknown"):
            num = len(encode_cmd)
            encode_cmd.insert(num-2, "-metadata")
            encode_cmd.insert(num-1, "album=" + release_info.title)
        if (len(release_info.artist) > 0 and release_info.artist != "Unknown"):
            num = len(encode_cmd)
            encode_cmd.insert(num-2, "-metadata")
            encode_cmd.insert(num-1, "artist=" + release_info.artist)
        if (len(release_info.year) > 0 and release_info.year != "Unknown"):
            num = len(encode_cmd)
            encode_cmd.insert(num-2, "-metadata")
            encode_cmd.insert(num-1, "year=" + release_info.year)
        if (len(title) > 0):
            num = len(encode_cmd)
            
            encode_cmd.insert(num-2, "-metadata")
            encode_cmd.insert(num-1, "title=" + title)

        print(encode_cmd)
        # ffmpeg -hide_banner -v error -i "title_t00.mkv" -ss "$start" -to "$end" -map 0:a:0 -vn -c:a flac -y "$out"

        try:
            print(f"Encoding {output_file}")
            result = subprocess.run(encode_cmd)
        except TypeError:
            print("TypeError, moving on")

        print("Encoding complete")
        i = i + 1

