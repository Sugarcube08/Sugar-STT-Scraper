import os
import json

def verify_chunks(dataset_folder):
    labels_file = os.path.join(dataset_folder, "labels.json")
    audio_folder = os.path.join(dataset_folder, "audio")

    # Load labels.json
    if not os.path.exists(labels_file):
        print("Error: labels.json not found.")
        return

    with open(labels_file, "r") as f:
        labels = json.load(f)

    # Get expected chunk filenames from labels.json
    expected_chunks = set(labels.keys())

    # Get actual chunk filenames in the audio folder
    if not os.path.exists(audio_folder):
        print("Error: Audio folder not found.")
        return

    actual_chunks = set(f for f in os.listdir(audio_folder) if f.endswith(".ogg"))

    # Compare the sets
    missing_chunks = expected_chunks - actual_chunks  # Chunks in labels.json but not in folder
    extra_chunks = actual_chunks - expected_chunks  # Chunks in folder but not in labels.json

    # Output results
    print(f"Total Entries in labels.json: {len(expected_chunks)}")
    print(f"Total Chunks in Folder: {len(actual_chunks)}")

    if len(expected_chunks) == len(actual_chunks):
        print("✅ Equal number of chunks in labels.json and folder.")
    elif len(expected_chunks) > len(actual_chunks):
        print(f"⚠ Less chunks in folder! {len(missing_chunks)} missing chunks.")
    else:
        print(f"⚠ More chunks in folder! {len(extra_chunks)} extra chunks.")

    # Show details if discrepancies exist
    if missing_chunks:
        print("\nMissing Chunks (in labels.json but not in folder):")
        for chunk in missing_chunks:
            print(f"  - {chunk}")

    if extra_chunks:
        print("\nExtra Chunks (in folder but not in labels.json):")
        for chunk in extra_chunks:
            print(f"  - {chunk}")

# Example usage
dataset_folder = input("Enter dataset folder path: ").strip()
verify_chunks(dataset_folder)
