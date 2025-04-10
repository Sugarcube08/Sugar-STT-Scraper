import csv
import json
import os
import random
import shutil
import pandas as pd

def k_fold(dataset_path, output_path, fold):
    # Paths to input files and directories
    label_json_path = os.path.join(dataset_path, 'labels.json')
    label_csv_path = os.path.join(dataset_path, 'labels.csv')
    audio_path = os.path.join(dataset_path, 'audio')
    
    # Load audio chunks and labels
    audio_chunks = os.listdir(audio_path)  # List of audio filenames
    audio_chunks.sort()  # Ensure consistent ordering
    num_chunks = len(audio_chunks)
    
    # Load JSON labels
    with open(label_json_path, 'r') as f:
        label_json = json.load(f)
    
    # Create output directories
    train_dataset = os.path.join(output_path, 'train')
    os.makedirs(train_dataset, exist_ok=True)
    train_audio = os.path.join(train_dataset, 'audio')
    os.makedirs(train_audio, exist_ok=True)
    test_dataset = os.path.join(output_path, 'test')
    os.makedirs(test_dataset, exist_ok=True)
    test_audio = os.path.join(test_dataset, 'audio')
    os.makedirs(test_audio, exist_ok=True)
    
    # Determine the number of test chunks
    test_chunk_count = num_chunks // fold
    test_indices = random.sample(range(num_chunks), test_chunk_count)
    
    # Split data into test and train sets
    test_labels = {}
    train_labels = {}
    
    for i, chunk in enumerate(audio_chunks):
        chunk_path = os.path.join(audio_path, chunk)
        if i in test_indices:
            test_labels[chunk] = label_json.get(chunk, {})
            shutil.copy(chunk_path, test_audio)
        else:
            train_labels[chunk] = label_json.get(chunk, {})
            shutil.copy(chunk_path, train_audio)
    
    # Save test labels to JSON
    with open(os.path.join(test_dataset, 'test_labels.json'), 'w') as f:
        json.dump(test_labels, f, indent=4)
    
    # Save train labels to JSON
    with open(os.path.join(train_dataset, 'train_labels.json'), 'w') as f:
        json.dump(train_labels, f, indent=4)
    
    # Process CSV and save filtered data
    with open(label_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames  # Dynamically get fieldnames from the input CSV
        test_csv_rows = []
        train_csv_rows = []
        
        for row in reader:
            chunk = row['Chunk']
            if chunk in test_labels:
                test_csv_rows.append(row)
            else:
                train_csv_rows.append(row)

    # Write test CSV
    with open(os.path.join(test_dataset, 'test_labels.csv'), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # Use dynamic fieldnames
        writer.writeheader()
        writer.writerows(test_csv_rows)

    # Write train CSV
    with open(os.path.join(train_dataset, 'train_labels.csv'), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # Use dynamic fieldnames
        writer.writeheader()
        writer.writerows(train_csv_rows)
        
    rename_and_update_labels(train_dataset, 'train')
    rename_and_update_labels(test_dataset, 'test')
        

def rename_and_update_labels(dataset_folder, label):
    """
    Renames all audio files in the dataset folder to continuous numbering,
    updates the labels.json file accordingly, and regenerates the labels.csv file.
    """
    labels_file = os.path.join(dataset_folder, f"{label}_labels.json")
    audio_folder = os.path.join(dataset_folder, "audio")
    labels_csv_path = os.path.join(dataset_folder, f"{label}_labels.csv")

    if not os.path.exists(labels_file):
        print("❌ Error: labels.json not found.")
        return

    if not os.path.exists(audio_folder):
        print("❌ Error: audio folder not found.")
        return

    # Load existing labels
    with open(labels_file, "r") as f:
        labels = json.load(f)

    # Get all audio files and sort them numerically
    chunks = sorted(
        [f for f in os.listdir(audio_folder) if f.endswith(".ogg")],
        key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')
    )

    new_labels = {}
    for index, chunk in enumerate(chunks, start=1):
        old_path = os.path.join(audio_folder, chunk)
        new_name = f"{index}.ogg"
        new_path = os.path.join(audio_folder, new_name)

        # Rename the audio file
        os.rename(old_path, new_path)

        # Update the labels with the new name
        if chunk in labels:
            new_labels[new_name] = labels[chunk]

    # Save the updated labels to the JSON file
    with open(labels_file, "w") as f:
        json.dump(new_labels, f, indent=4)

    # Regenerate the labels.csv file
    print("Updating labels.csv file...")
    data = []
    for chunk, words in new_labels.items():
        for word_info in words:
            data.append({
                "Chunk": chunk,
                "Word": word_info["word"],
                "Start Time": word_info["start"],
                "End Time": word_info["end"]
            })

    # Write the updated labels.csv
    df = pd.DataFrame(data, columns=["Chunk", "Word", "Start Time", "End Time"])
    df.to_csv(labels_csv_path, index=False)
    print("✅ Audio files renamed, labels.json and labels.csv updated successfully!")
 