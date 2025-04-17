import os
import json
import pandas as pd


def load_labels(label_path):
    """Load labels from label.json"""
    if os.path.exists(label_path):
        with open(label_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_labels(label_path, labels):
    """Save updated labels to label.json"""
    with open(label_path, "w", encoding="utf-8") as file:
        json.dump(labels, file, indent=4, ensure_ascii=False)


def update_labels_csv(dataset_path, labels):
    """Update labels.csv based on the updated labels.json"""
    labels_csv_path = os.path.join(dataset_path, "labels.csv")
    data = []

    for chunk, text in labels.items():
        data.append({
            "Chunk": chunk,
            "Transcription": text
        })

    # Write the updated labels.csv
    df = pd.DataFrame(data)
    df.to_csv(labels_csv_path, index=False)
    print(" labels.csv file created successfully!")


def auto_clean_dataset(dataset_path):
    """
    Automatically remove duplicate chunks and labels from the dataset.
    """
    # Paths
    audio_folder = os.path.join(dataset_path, "audio")
    labels_file = os.path.join(dataset_path, "labels.json")

    # Load labels
    labels = load_labels(labels_file)

    # List all audio chunks
    audio_chunks = sorted(
        (f for f in os.listdir(audio_folder) if f.endswith(".wav")),
        key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')
    )

    if not audio_chunks:
        print("No audio chunks found.")
        return

    # Identify duplicates
    unique_chunks = set()
    duplicates = []

    for chunk in audio_chunks:
        if chunk in unique_chunks:
            duplicates.append(chunk)
        else:
            unique_chunks.add(chunk)

    if not duplicates:
        print("No duplicate chunks found.")
        return

    # Remove duplicate chunks and their labels
    removed_files = 0
    for chunk in duplicates:
        chunk_path = os.path.join(audio_folder, chunk)

        # Remove file
        if os.path.exists(chunk_path):
            os.remove(chunk_path)
            removed_files += 1
            print(f"✅ Removed duplicate: {chunk}")

        # Remove label entry
        if chunk in labels:
            del labels[chunk]
            print(f"📝 Removed label entry for duplicate: {chunk}")

    # Save updated labels
    save_labels(labels_file, labels)

    # Update labels.csv
    update_labels_csv(dataset_path, labels)

    print(f"\n✅ Auto-clean complete! {removed_files} duplicate files removed.")


def clean_dataset(dataset_path):
    """Remove selected chunks and update labels.json and labels.csv"""

    # Paths
    audio_folder = os.path.join(dataset_path, "audio")
    labels_file = os.path.join(dataset_path, "labels.json")

    # Load labels
    labels = load_labels(labels_file)

    # List all audio chunks
    audio_chunks = sorted(
        (f for f in os.listdir(audio_folder) if f.endswith(".wav")),
        key=lambda x: int(x.split(".")[0]) if x.split(".")[0].isdigit() else float('inf')
    )

    if not audio_chunks:
        print("No audio chunks found.")
        return

    # Print all chunks and their transcriptions
    print("\nCurrent chunks and transcriptions:")
    for chunk in audio_chunks:
        text = labels.get(chunk, "No transcription")
        print(f"{chunk}: {text}")

    # Get chunks to remove
    to_remove = input("\nEnter chunk numbers to remove (comma-separated): ").strip()
    if not to_remove:
        print("No chunks selected for removal.")
        return

    # Process each chunk
    removed_files = 0
    for chunk_num in to_remove.split(","):
        chunk_num = chunk_num.strip()
        if not chunk_num.isdigit():
            continue

        chunk = f"{chunk_num}.wav"
        chunk_path = os.path.join(audio_folder, chunk)

        # Remove file
        if os.path.exists(chunk_path):
            os.remove(chunk_path)
            removed_files += 1
            print(f"✅ Removed: {chunk}")

        # Remove label entry
        if chunk in labels:
            del labels[chunk]
            print(f"📝 Removed label entry for: {chunk}")

    if removed_files == 0:
        print("No files were removed.")
        return

    # Save updated labels
    save_labels(labels_file, labels)

    # Update labels.csv
    update_labels_csv(dataset_path, labels)

    print(f"\n✅ Clean complete! {removed_files} files removed.")


# Example usage
if __name__ == "__main__":
    dataset_path = input("Enter dataset path: ").strip()
    if not os.path.exists(dataset_path):
        print("Error: Dataset path not found.")
        exit(1)

    mode = input("Choose mode (1: Manual clean, 2: Auto clean): ").strip()
    if mode == "1":
        clean_dataset(dataset_path)
    elif mode == "2":
        auto_clean_dataset(dataset_path)
    else:
        print("Invalid mode selected.")
