import os
import json
import shutil


def read_jsonfiles_in_directory(directory):
    """
    Reads json data in all files in the selected directory

    Parameters:
    directory: name of directory to read from
    returns list of json objects
    """

    data_list = []

    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):  # Process only JSON files
            filepath = os.path.join(directory, filename)

            # Open and read the JSON file
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)  # Deserialize JSON to a Python object
                data["filename"] = filename
                data_list.append(data)  # Add the deserialized data to the list

    return data_list


def get_files_in_directory(directory):
    """
    list files in selected directory

    Parameters:
    directory: name of directory to read from
    return list of filenames
    """
    data_list = []
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        data_list.append(filename)

    return data_list


def move_file(filename, source_directory, destination_directory):
    """
    move file

    Parameters:
    filename: name of file to be moved
    source_directory: directory where filename is located
    destination_directory: file is moved to this directory
    directory: name of directory to read from

    """
    if not destination_directory.endswith("\\"):
        destination_directory += "\\"
    if not source_directory.endswith("\\"):
        source_directory += "\\"

    moved_filename = destination_directory + os.path.basename(filename)
    # Check if the destination file exists
    if os.path.exists(moved_filename):
        print(f"File {moved_filename} already exists. It will be overwritten.")
        os.remove(moved_filename)

    move_filename = source_directory + os.path.basename(filename)
    # Move the file
    shutil.move(move_filename, moved_filename)
    print(f"Moved {move_filename} to {moved_filename}")


def save_json_document_to_file(document, filename):
    """
    save_json_document_to_file(document, filename)

    Parameters:
    document: json object
    filename: name of file to save

    """

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=4)
