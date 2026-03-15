import os
from dataclasses import dataclass
import release_info

if __name__ == "__main__":
    # Initialize catalog_vinyl.csv with header if it doesn't exist
    if not os.path.exists('catalog_vinyl.csv'):
        with open('catalog_vinyl.csv', 'w', encoding='utf-8', newline='') as f:
            f.write("ID,Artist,Title,Year,Format,Packaging,Label,Catalog Number,Country,Barcode,URL,Source\n")
        print("Created catalog_vinyl.csv with header row.")

    while True:
        upc_code = input("Enter UPC code, catalog number, or Artist:Title (or 'q' to quit): ").strip()
        if upc_code.lower() == 'q':
            print("Exiting.")
            break
        
        master_record = release_info.ReleaseInfo()
        release = None

        release = master_record.find_release_on_discogs(upc_code)
 
        if release:
            csvline = str(master_record)
            # Append the CSV line to catalog_vinyl.csv
            try:
                with open('catalog_vinyl.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write(csvline + '\n')
                print("Appended release to catalog_vinyl.csv")
            except Exception as e:
                print(f"Failed to append to catalog_vinyl.csv: {e}")

        else:
            print(f"Discogs returned a result with no releases for UPC code or catalog number: {upc_code}")
