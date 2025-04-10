# Sugar-STT-Scraper 🎤🔤
with
# 🧹Dataset Cleaning Script

**Sugar-STT-Scraper** is a powerful tool for transcribing speech from video and audio files into text. It leverages multiple technologies to enhance the audio quality, split long audio into smaller chunks, and transcribe the speech using Speech-to-Text (STT) models. The tool is specifically designed for preparing datasets for speech-to-text applications. 🧑‍💻💡

---

## Features ✨
- 🎬 **Extracts audio** from video files (MP4, MKV, AVI, etc.).
- 🎶 **Enhances audio** by applying a low-pass filter to remove high-frequency noise.
- ⏩ **Adjusts audio speed** and increases volume.
- 🎧 **Splits long audio** into smaller chunks (max 5 seconds).
- 🔄 Supports both **sequential and parallel transcription**.
- 🕰️ Organizes transcriptions with **word-level timestamps**.
- 📁 Allows **dataset creation** and **appending to existing datasets**.
- 🔽 Provides **progress bars** and **logs** for better tracking.
- 📂 **Dual Label Files:** Generates both `labels.json` and `labels.csv` for compatibility.
- 🌐 **YouTube URL Support:** Download and process audio directly from YouTube videos.
- 🔢 **K-Fold Dataset Splitting:** Automatically splits datasets into training and testing sets.
- 🧹 **Dataset Cleaning Script:** Selectively delete audio chunks and update labels.

---

## ✨ New Features (Updated on 04-04-2025) ✨
1. **Dual Label Files:**
   - Both `labels.json` and `labels.csv` are now generated for better usability.
2. **Dataset Modes:**
   - Local file mode: Process audio/video files directly.
   - YouTube URL mode: Download and process audio from YouTube videos.
3. **K-Fold Dataset Splitting:**
   - Automatically split datasets into training and testing sets using K-Fold.
4. **Audio Enhancements:**
   - Low-pass filtering for noise reduction.
   - Speed adjustment and volume increase options.
5. **Parallel Processing:**
   - Enable parallel transcription for faster processing.

---

## Requirements ⚙️
Before running the script, make sure you have the following installed:
- **Python 3.7+** 🐍
- **ffmpeg** (for audio extraction from video files) 🎥🎶
- **pydub** (for audio manipulation) 🔊
- **SpeechRecognition** (for speech-to-text transcription) 🗣️
- **tqdm** (for progress bars) ⏳
- **concurrent.futures** (for parallel processing) 🔄

To install the required Python libraries, you can use the provided `requirements.txt`:

```bash
pip install -r requirements.txt 
```

---

## Installation 🔧

1. Clone the repository:

```bash
git clone https://github.com/sugarcube08/Sugar-STT-Scraper.git
cd Sugar-STT-Scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

You also need to have ffmpeg installed on your system. You can install it from the FFmpeg official site or use a package manager.

For Linux (Ubuntu):
```bash
sudo apt-get install ffmpeg
```

For macOS (using Homebrew):
```bash
brew install ffmpeg
```

For Windows, download the binaries from the FFmpeg website and add it to your system’s PATH.

---

## Usage 🖥️

To use the tool, run the script with Python:
```bash
python run.py
```

The script will guide you through several prompts:

1. **Dataset Type:** Choose whether you are creating a new dataset or appending to an existing one.
2. **Mode:** Choose between Local file mode or YouTube URL mode.
3. **Input Path:** Provide the path to the video/audio file or YouTube URL.
4. **Speed Factor:** Adjust the speed of the audio (e.g., 1.0 for normal speed, 1.5 for faster, or 0.8 for slower).
5. **Volume Increase:** Optionally, increase the audio volume.
6. **Parallel Processing:** Choose if you want to enable parallel transcription for faster processing.

---

## Output 📊

The script will generate a dataset folder that contains:
- **Audio chunks** in the `audio/` subfolder.
- **Dual label files:**
  - `labels.json` with transcriptions and word-level timestamps for each chunk.
  - `labels.csv` for compatibility with spreadsheet tools.

---

## Dataset Cleaning Script 🧹

This script helps you clean up unwanted audio chunks and their corresponding labels from the dataset.

### Features
- ✅ Lists available chunks 📜 (sorted sequentially).
- ✅ Allows selective deletion 🗑️.
- ✅ Removes audio files 🎵 from the `audio/` folder.
- ✅ Updates both `labels.json` and `labels.csv` automatically.

### How to Use
1. Run the script:
   ```bash
   python data_cleaner.py
   ```
2. Enter the dataset folder path 📂 when prompted.
3. View the list of available chunks 🔢.
4. Enter chunk numbers to delete (comma-separated) ❌.
5. The script will:
   - 🚮 Delete the selected chunks.
   - ✏️ Remove their labels from `labels.json` and `labels.csv`.
   - ✅ Confirm cleanup success.

---

## Example Usage
```bash
Enter dataset path: /path/to/dataset
📜 Available Chunks:
1  2  3  5  6  8  9

Enter chunk numbers to remove (comma-separated): 3,8
✅ Removed: 3.ogg
📝 Removed label entry for 3.ogg
✅ Removed: 8.ogg
📝 Removed label entry for 8.ogg

🎉 Cleanup complete! 2 files removed.
```

---

## Folder Structure 📂
```
/dataset
 ├── audio/ 🎵       # Folder containing .ogg chunks
 ├── labels.json 📝    # File storing chunk labels
 ├── labels.csv 📝    # File storing chunk labels in CSV format
```

---

## Contributing 🤝

Feel free to fork this project, submit issues, or create pull requests to contribute to its development. 🌱

---

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

---

## ☕ Support Me

If you like this project, consider buying me a coffee!
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20Me-orange?style=flat-square&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/sugarcube08)

---

## Don't Forget To Subscribe
### Click on the Following Buttons:
[![YouTube Banner](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/@SugarCode-Z?sub_confirmation=1)
[![Instagram Banner](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://www.instagram.com/sugarcodez)
[![WhatsApp Banner](https://img.shields.io/badge/WhatsApp-%25D366.svg?logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029Vb5fFdzKgsNlaxFmhg1T)
