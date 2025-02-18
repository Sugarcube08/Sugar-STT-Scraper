# Sugar-STT-Scraper 🎤🔤
with
# 🔍 Verifier Program 

**Sugar-STT-Scraper** is a powerful tool for transcribing speech from video and audio files into text. It leverages multiple technologies to enhance the audio quality, split long audio into smaller chunks, and transcribe the speech using Speech-to-Text (STT) models. The tool is specifically designed for preparing datasets for speech-to-text applications. 🧑‍💻💡

## Features ✨
- 🎬 **Extracts audio** from video files (MP4, MKV, AVI, etc.).
- 🎶 **Enhances audio** by applying a low-pass filter to remove high-frequency noise.
- ⏩ **Adjusts audio speed** and increases volume.
- 🎧 **Splits long audio** into smaller chunks (max 5 seconds).
- 🔄 Supports both **sequential and parallel transcription**.
- 🕰️ Organizes transcriptions with **word-level timestamps**.
- 📁 Allows **dataset creation** and **appending to existing datasets**.
- 🔽 Provides **progress bars** and **logs** for better tracking.

## Requirements ⚙️
Before running the script, make sure you have the following installed:
- **Python 3.7+** 🐍
- **ffmpeg** (for audio extraction from video files) 🎥🎶
- **pydub** (for audio manipulation) 🔊
- **SpeechRecognition** (for speech-to-text transcription) 🗣️
- **tqdm** (for progress bars) ⏳
- **concurrent.futures** (for parallel processing) 🔄

To install the required Python libraries, you can use the provided `requirements.txt`:

```
pip install -r requirements.txt 
```
Installation 🔧

1. Clone the repository:



You can clone this repository using Git:
```
git clone https://github.com/sugarcube08/Sugar-STT-Scraper.git
cd Sugar-STT-Scraper
```
2. Install dependencies:



Install the necessary dependencies by running the following command in your terminal:
```
pip install -r requirements.txt
```
You also need to have ffmpeg installed on your system. You can install it from the FFmpeg official site or use a package manager.

For Linux (Ubuntu):
```
sudo apt-get install ffmpeg
```
For macOS (using Homebrew):
```
brew install ffmpeg
```
For Windows, download the binaries from the FFmpeg website and add it to your system’s PATH.

3. Usage 🖥️



To use the tool, run the script with Python:
```
python run.py
```
The script will guide you through several prompts:

1. Dataset Type: Choose whether you are creating a new dataset or appending to an existing one.


2. Mode: Choose whether you want to create a new dataset or append to an existing one.


3. Input Path: Provide the path to the video/audio file you want to transcribe.


4. Speed Factor: Adjust the speed of the audio (e.g., 1.0 for normal speed, 1.5 for faster, or 0.8 for slower).


5. Volume Increase: Optionally, increase the audio volume.


6. Parallel Processing: Choose if you want to enable parallel transcription for faster processing.


7. Output 📊



The script will generate a dataset folder that contains:

Audio chunks in the audio/ subfolder.

A labels.json file with transcriptions and word-level timestamps for each chunk.


Effectiveness 🚀

Sugar-STT-Scraper is highly effective for transcription tasks, especially when dealing with noisy audio or large files. By splitting long files into smaller chunks and enhancing the audio, it ensures better accuracy for speech-to-text models. Parallel processing also improves speed, making it ideal for large datasets. ⚡

Pros 👍:

🧑‍💻 Efficient for handling large video/audio files.

🎧 Improved transcription accuracy due to audio enhancement (low-pass filtering).

🕰️ Provides word-level timestamps, which is useful for training STT models.

🛠️ Customizable (audio speed, volume increase).


Cons 👎:

🌐 Requires a stable internet connection for the Speech-to-Text API.

🔉 Dependent on the quality of the original audio.


Cautions ⚠️

Ensure the input files are compatible: The script supports common video and audio formats like MP4, MKV, AVI, and WAV. Other formats may require conversion.

Audio file size: Large files can be resource-intensive. If running on a low-resource machine, consider adjusting parameters such as speed or using parallel processing for faster processing.

Dependencies: Ensure that ffmpeg, pydub, and other dependencies are properly installed, as they are critical for the script’s functionality.



Here's the README.md section for the Verifier Program, which you can append to the existing documentation for Sugar-STT-Scraper.


---

🔍 Verifier Program – Check Dataset Integrity

The Verifier Program ensures that all transcribed chunks listed in labels.json actually exist in the dataset folder. It helps identify missing and extra chunks, ensuring dataset consistency.

🛠 How It Works

Reads labels.json to get a list of expected audio chunks.

Scans the audio/ folder to check actual .ogg files.

Compares both lists and reports:

✅ If the number of chunks matches.

⚠ If chunks are missing (listed in labels.json but not in the folder).

⚠ If there are extra chunks (exist in the folder but not in labels.json).



📌 Usage

1. Run the script
```
python verifier.py
```

2. Enter the dataset folder path when prompted.


3. Check the output for missing or extra chunks.



📊 Example Output


``
Total Entries in labels.json: 100
Total Chunks in Folder: 98
⚠ Less chunks in folder! 2 missing chunks.

Missing Chunks (in labels.json but not in folder):
  - 23.ogg
  - 45.ogg 
``

OR

``
Total Entries in labels.json: 50
Total Chunks in Folder: 55
⚠ More chunks in folder! 5 extra chunks.

Extra Chunks (in folder but not in labels.json):
  - 102.ogg
  - 105.ogg
``

OR

``
Total Entries in labels.json: 75
Total Chunks in Folder: 75
✅ Equal number of chunks in labels.json and folder.
``


🔗 Integration with Sugar-STT-Scraper

This verifier is a post-processing tool to ensure dataset quality after running Sugar-STT-Scraper. Run it before training to avoid missing data issues.


---


Contributing 🤝

Feel free to fork this project, submit issues, or create pull requests to contribute to its development. 🌱

License 📄

This project is licensed under the MIT License - see the LICENSE file for details.



---

#Made with ❤️ by SugarCube.#
---
Feel free to customize the repository and use it for your own bulk audio volume adjustments! 😄🎶

---
## ☕ Support Me
If you like this project, consider buying me a coffee!
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20Me-orange?style=flat-square&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/sugarcube08)
---
