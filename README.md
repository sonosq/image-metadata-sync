# image-metadata-sync

This Python script updates the metadata of photos and videos based on JSON metadata files. It ensures that file extensions are lowercase and applies metadata such as title, creation date, modification date, and GPS coordinates.

## Features

- Converts file extensions to lowercase.
- Reads metadata from JSON files.
- Formats date strings to a specific format.
- Retrieves existing metadata using `exiftool`.
- Applies new metadata to files if different from the existing metadata.
- Supports image and video files with extensions `.jpg`, `.jpeg`, `.png`, `.mp4`, and `.mov`.
- Provides verbose output for detailed logging.

## Requirements

- Python 3.x
- `exiftool` installed and available in the system PATH.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/sonosq/image-metadata-sync.git
    cd image-metadata-sync
    ```

2. Install the required dependencies:

    ```sh
    pip3 install -r requirements.txt
    ```

3. Ensure `exiftool` is installed:

    ```sh
    sudo apt-get install exiftool  # For Debian-based systems
    # or
    brew install exiftool  # For macOS
    ```

## Usage

1. Prepare your photos and metadata files:
    - Place your photos and videos in a directory.
    - Ensure each photo or video has a corresponding JSON metadata file in a subdirectory named `metadata`.

2. Run the script:

    ```sh
    python exif_ch.py --photos-directory /path/to/photos --verbose
    ```

    - `--photos-directory`: The directory containing the photos and videos.
    - `--verbose`: Enable verbose output (optional).

## Example

```sh
python exif_ch.py --photos-directory /home/user/photos --verbose
```

This will process all photos and videos in the specified directory, update their metadata based on the corresponding JSON files in the metadata subdirectory, and print detailed logs of the operations performed.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


