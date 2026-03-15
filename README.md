# AV-Utilities
## AudioExcavator.py

### Usage

```bash
python3 AudioExcavator.py input_file.mkv output_folder artist album
```

#### Arguments

- `input_file`: Path to the input .mkv file containing audio chapters
- `output_folder`: Directory where the extracted FLAC files will be saved
- `artist`: Artist name used for MusicBrainz lookup
- `album`: Album name used for MusicBrainz lookup

#### Description

Attempts to read a .mkv file, determine the chapters and their start/end times. Looks up the artist/album info on musicbrainz.org. If multiple releases are found, prompts the user to select a release. Given a selected release, fetches the track info from musicbrainz and matches track info to the mkv chapters.

Finally, it uses ffmpeg to encode each chapter as a lossless FLAC file, adding ID3 tags to each audio file.

## cd_scanner.py
### Usage
```bash
python3 cd_scanner.py
```
Prompts the user for release information for lookup on musicbrainz.org. When multiple releases are found, user is prompted to select the correct release.  Once the user chooses a release, the album information is appended to the file catalog_cd.csv.

#### Release Information Inputs

- **Barcode**: If input is all digits with 12 or 13 digits assumes barcode
- **Artist:Title**: If input is in the format Artist:Title, splits the input and queries by artist and title
- **Catalog Number**: Otherwise, any other string is assumed to be a catalog ID and attempts to query by catalog ID

## lp_scanner.py
### Usage
```bash
python3 lp_scanner.py
```
Prompts the user for release information for lookup on discogs.com. When multiple releases are found, user is prompted to select the correct release.  Once the user chooses a release, the album information is appended to the file catalog_lp.csv.

#### Release Information Inputs

- **Barcode**: If input is all digits with 12 or 13 digits assumes barcode
- **Artist:Title**: If input is in the format Artist:Title, splits the input and queries by artist and title
- **Catalog Number**: Otherwise, any other string is assumed to be a catalog ID and attempts to query by catalog ID

## dv_encode_prep.py
### Usage
```bash
python3 cd_scanner.py
```
Prompts the user for release information for lookup on musicbrainz.org. When multiple releases are found, user is prompted to select the correct release.  Once the user chooses a release, the album information is appended to the file catalog_cd.csv.

#### Release Information Inputs

- **Barcode**: If input is all digits with 12 or 13 digits assumes barcode
- **Artist:Title**: If input is in the format Artist:Title, splits the input and queries by artist and title
- **Catalog Number**: Otherwise, any other string is assumed to be a catalog ID and attempts to query by catalog ID