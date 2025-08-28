import json
import os


def jsonConvert(source_dir, target_dir, source_name):
    for entry in os.listdir(source_dir):
        full_path = os.path.join(source_dir, entry)

        if os.path.isdir(full_path):
            continue

        # Read the existing JSON file
        print(f"Opening file: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        # Rename 'Embedding' to 'text_to_embed'
        data["text_to_embed"] = data.pop("Embedding")

        # Add a new field 'tokensize' (let's assume it should be the length of 'Content')
        data["token_size"] = int(len(data["Content"].split()))

        data["source"] = source_name

        filename, extension = os.path.splitext(entry)
        new_full_path = os.path.join(target_dir, filename + extension)

        lowercased_data = {k.lower(): v for k, v in data.items()}
        # Write the modified data to a new JSON file
        print(f"Writing file: {new_full_path}")
        with open(new_full_path, "w", encoding="utf-8") as f:
            json.dump(lowercased_data, f, ensure_ascii=False, indent=4)
            f.close()
