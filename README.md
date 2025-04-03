# Sugar-STT-Scraper 🎤🔤
with
# 🧹Dataset Cleaning Script


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

## ✨ New Feature Update ✨
- Now you have 2 modes to choose from(Updated on 03-04-2025): 
  - 1. Local file mode: if you have video or audio
  - 2. Youtube Url mode: if you want to use Youtube video as input and make data set out of it.

- Now You have dual label file,
  - 1. labels.json
  - 2. labels.csv


## ✨ New Update ✨
- Now you have 2 modes to choose from(Updated on 03-04-2025): 
  - 1. Local file mode: if you have video or audio
  - 2. Youtube Url mode: if you want to use Youtube video as input and make data set out of it.

- Now You have dual label file(Updated on 04-04-2025)
  - 1. labels.json
  - 2. labels.csv


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


# 🧹Dataset Cleaning Script

This script helps you clean up unwanted audio chunks and their corresponding labels from the dataset.


---

✨ Features

✅ Lists available chunks 📜 (sorted sequentially)
✅ Allows selective deletion 🗑️
✅ Removes audio files 🎵 from the audio/ folder
✅ Updates label.json 📝 automatically


---

🚀 How to Use

1️⃣ Run the script:
```
python clean_dataset.py
```
2️⃣ Enter the dataset folder path 📂 when prompted
3️⃣ View the list of available chunks 🔢
4️⃣ Enter chunk numbers to delete (comma-separated) ❌
5️⃣ The script will:

🚮 Delete the selected chunks

✏️ Remove their labels from label.json

✅ Confirm cleanup success



---

📝 Example Usage
```
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

📂 Folder Structure
```
/dataset
 ├── audio/ 🎵       # Folder containing .ogg chunks
 ├── label.json 📝    # File storing chunk labels
 ├── labels.csv 📝    # File storing chunk labels in csv format
```
Happy cleaning! 🧹😃



Contributing 🤝

Feel free to fork this project, submit issues, or create pull requests to contribute to its development. 🌱

License 📄

This project is licensed under the MIT License - see the LICENSE file for details.



---
## Made with ❤️ by SugarCube.
---
Feel free to customize the repository and use it for your own bulk audio volume adjustments! 😄🎶

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
