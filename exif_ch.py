import os
import json
import subprocess
from datetime import datetime
import argparse

def convert_extension_to_lowercase(file_path, verbose=False):
    directory, filename = os.path.split(file_path)
    name, extension = os.path.splitext(filename)
    new_filename = f"{name}{extension.lower()}"
    new_file_path = os.path.join(directory, new_filename)
    os.rename(file_path, new_file_path)
    if verbose:
        print(f"Converted extension to lowercase for {file_path}")
    return new_file_path

def read_metadata(json_file_path, verbose=False):
    with open(json_file_path, 'r') as file:
        metadata = json.load(file)
    if verbose:
        print(f"Read metadata from {json_file_path}")
    return metadata

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y, %H:%M").strftime("%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None

def get_existing_metadata(file_path, verbose=False):
    result = subprocess.run(['exiftool', '-j', file_path], capture_output=True, text=True)
    metadata = json.loads(result.stdout)[0]
    if verbose:
        print(f"Retrieved existing metadata for {file_path}")
    return metadata

def apply_metadata(file_path, metadata, verbose=False):
    creation_date = format_date(metadata["creationTime"]["formatted"])
    modification_date = format_date(metadata["modificationTime"]["formatted"])

    if not creation_date or not modification_date:
        if verbose:
            print(f"Invalid date format in metadata for {file_path}")
        return

    commands = [
        'exiftool',
        f'-Title={metadata.get("title", "")}',
        f'-CreationDate={creation_date}',
        f'-ModifyDate={modification_date}'
    ]

    if metadata['geoData']['latitude'] is not None and metadata['geoData']['longitude'] is not None:
        commands.append(f'-GPSLatitude={metadata["geoData"]["latitude"]}')
        commands.append(f'-GPSLongitude={metadata["geoData"]["longitude"]}')

    commands.append(file_path)
    subprocess.run(commands, stderr=subprocess.PIPE)
    if verbose:
        print(f"Metadata updated for {file_path}")

def is_metadata_different(existing_metadata, new_metadata):
    creation_date = format_date(new_metadata["creationTime"]["formatted"])
    modification_date = format_date(new_metadata["modificationTime"]["formatted"])

    return (
        existing_metadata.get('Title') != new_metadata.get("title", "") or
        existing_metadata.get('CreationDate') != creation_date or
        existing_metadata.get('ModifyDate') != modification_date or
        (existing_metadata.get('GPSLatitude') != new_metadata["geoData"]["latitude"] and
         existing_metadata.get('GPSLongitude') != new_metadata["geoData"]["longitude"])
    )

def is_valid_image(file_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
    return any(file_path.lower().endswith(ext) for ext in valid_extensions)

def process_files(photos_directory, metadata_directory, verbose=False):
    for filename in os.listdir(photos_directory):
        if is_valid_image(filename):
            file_path = os.path.join(photos_directory, filename)
            json_file_path = os.path.join(metadata_directory, f"{filename}.json")

            # Ensure file extensions are lowercase
            try:
                file_path = convert_extension_to_lowercase(file_path, verbose)
            except Exception as e:
                if verbose:
                    print(f"Error converting extension to lowercase for {file_path}: {e}")
                continue

            if os.path.exists(json_file_path):
                try:
                    metadata = read_metadata(json_file_path, verbose)
                except Exception as e:
                    if verbose:
                        print(f"Error reading metadata from {json_file_path}: {e}")
                    continue

                try:
                    existing_metadata = get_existing_metadata(file_path, verbose)
                except Exception as e:
                    if verbose:
                        print(f"Error retrieving existing metadata for {file_path}: {e}")
                    continue

                if is_metadata_different(existing_metadata, metadata):
                    try:
                        apply_metadata(file_path, metadata, verbose)
                    except Exception as e:
                        if verbose:
                            print(f"Error applying metadata to {file_path}: {e}")
                        continue
                else:
                    if verbose:
                        print(f"Metadata for {file_path} is already up-to-date.")

    if not verbose:
        print("Completado")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update photo and video metadata.")
    parser.add_argument("--photos-directory", required=True, help="Directory containing the photos and videos.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    args = parser.parse_args()

    photos_directory = args.photos_directory
    metadata_directory = os.path.join(photos_directory, 'metadata')

    process_files(photos_directory, metadata_directory, args.verbose)
