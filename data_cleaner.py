import os
import json

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

def clean_dataset(dataset_path):
    """Remove selected chunks and update label.json"""

    # Paths
    audio_folder = os.path.join(dataset_path, "audio")
    label_path = os.path.join(dataset_path, "label.json")

    # Load labels
    labels = load_labels(label_path)

    # List available chunks (sorted numerically)
    available_chunks = sorted(
        (f for f in os.listdir(audio_folder) if f.endswith(".ogg")),
        key=lambda x: int(x.replace(".ogg", ""))
    )

    if not available_chunks:
        print("No audio chunks found.")
        return

    # Display available chunks
    print("\nAvailable Chunks:\n")
    print("  ".join(chunk.replace(".ogg", "") for chunk in available_chunks))
    print("\n")

    # Get user input
    chunk_numbers = input("Enter chunk numbers to remove (comma-separated): ").strip()
    if not chunk_numbers:
        print("No chunks specified. Exiting.")
        return

    chunks_to_remove = {f"{num.strip()}.ogg" for num in chunk_numbers.split(",")}

    # Process deletions
    removed_files = 0
    for chunk in chunks_to_remove:
        chunk_path = os.path.join(audio_folder, chunk)

        # Remove file
        if os.path.exists(chunk_path):
            os.remove(chunk_path)
            removed_files += 1
            print(f"✅ Removed: {chunk}")

        else:
            print(f"⚠️ Not found: {chunk}")

        # Remove label entry
        if chunk in labels:
            del labels[chunk]
            print(f"📝 Removed label entry for {chunk}")

    # Save updated labels
    save_labels(label_path, labels)

    print(f"\n✅ Cleanup complete! {removed_files} files removed.")

# Example usage
if __name__ == "__main__":
    dataset_path = input("Enter dataset path: ").strip()
    if os.path.exists(dataset_path):
        clean_dataset(dataset_path)
    else:
        print("Invalid path. Exiting.")
