import os
import json
import tempfile
import shutil
import logging
import speech_recognition as sr
import subprocess 
from pydub import AudioSegment, silence
from pydub.effects import low_pass_filter
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm 
import yt_dlp
import pandas as pd
import unidecode
from algorithms import algo


def print_banner():
    banner = """
    ***************************************************************
    *                                                             *
    *                   Welcome to Sugar-STT-Scraper              *
    *             Powered by SugarCube08 (Harsh Raikwar)          *
    *                                                             *
    ***************************************************************
    *                                                             *
    *   Sugar-STT-Scraper: Your ultimate Speech-to-Text tool      *
    *   Harnessing Excellent technology for Dataset Preparation   *
    *                                                             *
    ***************************************************************

      Let's unlock the power of speech and transform it into text!
        If you liked my Project Consider buying me a coffee 

    ***************************************************************
    """
    print(banner)
    
def download_audio(link, temp_folder):
    """
    Downloads the best-quality audio from the given link using yt_dlp and converts it to .wav format.

    Args:
        link (str): The URL of the audio/video to download.
        temp_folder (str): The folder where the downloaded audio will be saved.

    Returns:
        str: The absolute path to the downloaded audio file in .wav format, or None if the download fails.
    """
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio format available
        'outtmpl': os.path.join(temp_folder, 'temp.%(ext)s'),  # Output template for the file
        'restrictfilenames': True,  # Restrict filenames to ASCII characters
        'noplaylist': True,  # Download only a single video, not a playlist
        'nocheckcertificate': True,  # Do not check SSL certificates
        'ignoreerrors': True,  # Ignore errors during the download process
        'quiet': True,  # Suppress output
        'logtostderr': False,  # Do not log to stderr
        'no_warnings': True,  # Suppress warnings
        'no_call_home': True,  # Do not send tracking information to YouTube
        'no_color': True,  # Disable colored output
        'postprocessors': [  # Post-process the downloaded file
            {
                'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                'preferredcodec': 'wav',  # Convert to .wav format
                'preferredquality': '192',  # Set audio quality (optional)
            }
        ]
    }

    try:
        logging.info(f"Starting download from: {link}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(link, download=True)
            if result:
                downloaded_file = os.path.join(temp_folder, f"temp.wav")
                logging.info(f"Download completed: {downloaded_file}")
                return os.path.abspath(downloaded_file)
            else:
                logging.error("Download failed: No result returned by yt_dlp.")
                return None
    except Exception as e:
        logging.error(f"An error occurred during download: {e}")
        return None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def extract_audio(video_path, output_audio_path):
    output_dir = os.path.dirname(output_audio_path)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Extracting audio from {video_path}...")

    try:
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_audio_path
        ]
        subprocess.run(cmd, check=True)
        logging.info(f"Audio extracted: {output_audio_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during audio extraction: {e.stderr.decode('utf-8')}")
    except Exception as e:
        logging.error(f"Unexpected error during audio extraction: {e}")

def enhance_audio(input_path, output_path):
    logging.info(f"Enhancing audio: {input_path}")
    audio = AudioSegment.from_wav(input_path)
    reduced_noise_audio = low_pass_filter(audio, 3000) 
    reduced_noise_audio.export(output_path, format="wav")
    logging.info(f"Enhanced audio saved: {output_path}")
    return output_path
def adjust_speed(audio_path, output_path, speed_factor=1.0):
    if speed_factor == 1.0:
        logging.info(f"Speed factor is {speed_factor}, no speed adjustment needed for {audio_path}")
        return audio_path 
    logging.info(f"Adjusting speed to {speed_factor}x for {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    adjusted_audio = audio.speedup(playback_speed=speed_factor)

    adjusted_audio.export(output_path, format="wav")
    logging.info(f"Speed-adjusted audio saved: {output_path}")
    return output_path

def increase_volume(input_path, output_path, gain_db=5):
    logging.info(f"Increasing volume by {gain_db}dB for {input_path}")
    audio = AudioSegment.from_wav(input_path)
    increased_audio = audio + gain_db 
    increased_audio.export(output_path, format="wav")
    logging.info(f"Volume increased audio saved: {output_path}")
    return output_path

def split_audio(audio_path, output_folder, start_index=1, max_duration=5000):
    logging.info(f"Splitting audio: {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    chunks = silence.split_on_silence(audio,
        min_silence_len=50,                  # shorter silence considered
        silence_thresh=audio.dBFS - 16)

    final_chunks = []
    temp_chunk = AudioSegment.silent(duration=0)

    for chunk in chunks:
        if len(temp_chunk) + len(chunk) <= max_duration:
            temp_chunk += chunk
        else:
            final_chunks.append(temp_chunk)
            temp_chunk = chunk
    if len(temp_chunk) > 0:
        final_chunks.append(temp_chunk)

    os.makedirs(output_folder, exist_ok=True)
    chunk_paths = []

    for i, chunk in enumerate(tqdm(final_chunks, desc="Saving Chunks", unit="chunk"), start=start_index):
        chunk_path = os.path.join(output_folder, f"{i}.wav")  # Ensure .wav format
        chunk.export(chunk_path, format="wav")  # Export as .wav
        chunk_paths.append((chunk_path, len(chunk) / 1000))
        logging.info(f"Saved chunk: {chunk_path}")

    return chunk_paths

def transcribe_chunk(chunk_path,language_code=None):
    recognizer = sr.Recognizer()
    logging.info(f"Transcribing: {chunk_path}")

    with sr.AudioFile(chunk_path) as source:  # Directly use .wav file
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language=language_code)
            if language_code != 'en-US':
                text = unidecode.unidecode(text)
                logging.info(f"Transcription success: {text}")
            else:
                logging.info(f"Transcription success: {text}")
            return chunk_path, text
        except sr.UnknownValueError:
            logging.warning("Speech not recognized")
            return chunk_path, None
        except sr.RequestError:
            logging.error("STT service unreachable")
            return chunk_path, None

def transcribe_audio(chunks, parallel=False, language_code=None):
    labels = {}

    if parallel:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda x: transcribe_chunk(x[0], language_code), chunks))
    else:
        results = []
        for chunk in tqdm(chunks, desc="Transcribing Chunks", unit="chunk"):
            result = transcribe_chunk(chunk[0], language_code)  
            results.append(result)

    for chunk_path, text in results:
        if text:
            chunk_name = os.path.basename(chunk_path)
            labels[chunk_name] = text  # Just store the text directly
        else:
            os.remove(chunk_path)
            logging.info(f"Deleted untranscribed chunk: {chunk_path}")

    return labels


def csv_labels(label_file, dataset_folder):
    labels_json_path = os.path.join(dataset_folder, "labels.json")
    labels_csv_path = os.path.join(dataset_folder, "labels.csv")

    print("Creating labels.csv file...")
    # Read the JSON file
    with open(labels_json_path, "r") as f:
        labels = json.load(f)
    
    # Convert to DataFrame
    data = []
    for chunk, text in labels.items():
        data.append({
            "Chunk": chunk,
            "Transcription": text
        })
    
    # Create DataFrame and sort numerically by chunk number
    df = pd.DataFrame(data)
    df['ChunkNum'] = df['Chunk'].str.replace('.wav', '').astype(int)
    df.sort_values(by='ChunkNum', inplace=True)
    df.drop('ChunkNum', axis=1, inplace=True)
    df.to_csv(labels_csv_path, index=False)
    print(" labels.csv file created successfully!")


def rename_and_update_labels(dataset_folder):
    """
    Renames all audio files in the dataset folder to continuous numbering,
    updates the labels.json file accordingly, and regenerates the labels.csv file.
    """
    labels_file = os.path.join(dataset_folder, "labels.json")
    audio_folder = os.path.join(dataset_folder, "audio")
    labels_csv_path = os.path.join(dataset_folder, "labels.csv")

    if not os.path.exists(labels_file):
        print(" Error: labels.json not found.")
        return

    if not os.path.exists(audio_folder):
        print(" Error: audio folder not found.")
        return
       
    # Load existing labels
    with open(labels_file, "r") as f:
        existing_labels = json.load(f)

    # Get list of audio files
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav')]
    
    # Find the highest existing number to start appending from there
    existing_numbers = []
    for filename in existing_labels.keys():
        try:
            num = int(filename.replace('.wav', ''))
            existing_numbers.append(num)
        except ValueError:
            continue
    
    next_number = max(existing_numbers) + 1 if existing_numbers else 1

    # Process new files
    new_labels = {}
    for audio_file in audio_files:
        if audio_file not in existing_labels:
            new_name = f"{next_number}.wav"
            next_number += 1
            
            # Rename the file
            old_path = os.path.join(audio_folder, audio_file)
            new_path = os.path.join(audio_folder, new_name)
            os.rename(old_path, new_path)
            
            # Update labels
            if audio_file in existing_labels:
                new_labels[new_name] = existing_labels[audio_file]
        else:
            new_labels[audio_file] = existing_labels[audio_file]

    # Merge existing and new labels
    merged_labels = {**existing_labels, **new_labels}

    # Save updated labels
    with open(labels_file, "w") as f:
        json.dump(merged_labels, f, indent=4)

    # Update CSV file
    csv_labels(merged_labels, dataset_folder)
    print(" Audio files renamed, labels.json and labels.csv updated successfully!")


def safe_move(src, dst):
    """
    Safely move a file to a destination, handling existing file conflicts.
    If the destination exists, appends a number to the filename.
    """
    if not os.path.exists(dst):
        shutil.move(src, dst)
        return dst
    
    # If destination exists, find a new name
    base, ext = os.path.splitext(dst)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    new_dst = f"{base}_{counter}{ext}"
    shutil.move(src, new_dst)
    return new_dst

if __name__ == "__main__":
    print_banner()
    
    dataset_type = input("Choose dataset type:-\n1: Common Dataset\n2: Saperated Dataset(Training & Testing)\nOr Leave Empty for Common Dataset\n>> ").strip() or "1"    
    if dataset_type == "1":
        dataset_name = "Common"
        dataset_mode = input("Choose mode (1: Create New, 2: Append Existing): ").strip() or "1"
        input_mode = input("Choose input mode (1: Local files, 2: Youtube URLs): ").strip() or "1"
        temp_folder = os.path.abspath("temp")
        os.makedirs(temp_folder, exist_ok=True)            
        if input_mode == "1":
            input_path = input("Enter the path of video/audio file: ").strip() or "1"
        elif input_mode == "2":
            url = input("Enter the youtube url: ").strip()      
            input_path = download_audio(url, temp_folder)
        else: 
            print("Invalid input mode. Exiting.")               
               
        lang_dict = {
            "Afrikaans": "af-ZA",
            "Standard-Arabic": "ar",
            "Egypt": "ar-EG",
            "Gulf": "ar-AE",
            "Levantine": "ar-IL",
            "Maghreb": "ar-MA",
            "Modern Standard": "ar-001",
            "Bengali": "bn-IN",
            "Catalan": "ca-ES",
            "Simplified Chinese": "zh-CN",
            "Traditional Chinese": "zh-TW",
            "Hong Kong Chinese": "zh-HK",
            "Croatian": "hr-HR",
            "Czech": "cs-CZ",
            "Danish": "da-DK",
            "Dutch": "nl-NL",
            "Australia English": "en-AU",
            "India English": "en-IN",
            "Ireland English": "en-IE",
            "New Zealand English": "en-NZ",
            "Philippines English": "en-PH",
            "Singapore English": "en-SG",
            "South Africa English": "en-ZA",
            "United Kingdom English": "en-GB",
            "United States English": "en-US",
            "Finnish": "fi-FI",
            "Standard French": "fr-FR",
            "Canadian French": "fr-CA",
            "German": "de-DE",
            "Greek": "el-GR",
            "Gujarati": "gu-IN",
            "Hindi": "hi-IN",
            "Hungarian": "hu-HU",
            "Icelandic": "is-IS",
            "Italian": "it-IT",
            "Japanese": "ja-JP",
            "Kannada": "kn-IN",
            "Korean": "ko-KR",
            "Latvian": "lv-LV",
            "Lithuanian": "lt-LT",
            "Malay": "ms-MY",
            "Marathi": "mr-IN",
            "Nepali": "ne-IN",
            "Norwegian": "no-NO",
            "Polish": "pl-PL",
            "Standard Portuguese": "pt-PT",
            "Brazil Portuguese": "pt-BR",
            "Romanian": "ro-RO",
            "Russian": "ru-RU",
            "Serbian": "sr-RS",
            "Standard Spanish": "es-ES",
            "Mexico Spanish": "es-MX",
            "United States Spanish": "es-US",
            "Swahili": "sw-KE",
            "Swedish": "sv-SE",
            "Tamil": "ta-IN",
            "Telugu": "te-IN",
            "Thai": "th-TH",
            "Turkish": "tr-TR",
            "Ukrainian": "uk-UA",
            "Urdu": "ur-PK",
            "Vietnamese": "vi-VN",
            "Welsh": "cy-GB",
            "Yiddish": "yi",
        }
        languages = list(lang_dict.keys())
        language_codes = list(lang_dict.values())
        print("Choose the language of The Content:")
        for index, language in enumerate(languages, start=1):
            print(f"{index}: {language}")
        language_choice = int(input("Enter language number: ").strip())
        language_code = language_codes[language_choice-1]
        speed_factor = float(input("Enter speed factor (1.0 = normal, <1.0 = slow, >1.0 = fast): ").strip() or "1.0")
        parallel = input("Use parallel processing? (y for yes /n for no): ").strip().lower() == "y"
        
        if dataset_mode == "1":
            output_path = input("Enter output path (leave blank for current folder): ").strip() or os.getcwd()
            dataset_folder = os.path.join(output_path, f"{dataset_name}_dataset")
            audio_folder = os.path.join(dataset_folder, "audio")
            os.makedirs(audio_folder, exist_ok=True)
            labels_file = os.path.join(dataset_folder, "labels.json")
            existing_labels = {}
            start_index = 1
            logging.info(f"Creating new dataset at {dataset_folder}")
        
        elif dataset_mode == "2":
            dataset_folder = input("Enter existing dataset folder path: ").strip()
            audio_folder = os.path.join(dataset_folder, "audio")

            if not os.path.exists(audio_folder):
                logging.error("Audio folder not found.")
               

            labels_file = os.path.join(dataset_folder, "labels.json")
            if os.path.exists(labels_file):
                with open(labels_file, "r") as f:
                    existing_labels = json.load(f)
            else:
                existing_labels = {}

            existing_files = [f for f in os.listdir(audio_folder) if f.endswith(".wav")]
            start_index = max([int(f.split(".")[0]) for f in existing_files if f.split(".")[0].isdigit()], default=0) + 1
            logging.info(f"Appending to existing dataset at {dataset_folder}")

        else:
            logging.error("Invalid choice. Exiting.")
           
        increase_volume_choice = input("Do you want to increase the volume beyond original? (y for Yes / n for No): ").strip().lower() or "n"
        gain_db = 0
        if increase_volume_choice == "y":
            gain_db = float(input("Enter gain in dB (e.g., 5 for 5dB increase): ").strip())

        extracted_audio = os.path.join(dataset_folder, "temp.wav")
        if input_path.lower().endswith((".mp4", ".mp3", ".mkv", ".avi", ".mov", ".m4a")):
            extract_audio(input_path, extracted_audio)
        else:
            shutil.copy(input_path, extracted_audio)

        if not os.path.exists(extracted_audio):
            logging.error(f"Extracted audio file not found: {extracted_audio}")           

        enhanced_audio = enhance_audio(extracted_audio, extracted_audio)
        if gain_db > 0:
            enhanced_audio = increase_volume(enhanced_audio, extracted_audio, gain_db)
        adjusted_audio = adjust_speed(enhanced_audio, extracted_audio, speed_factor)    
        try:
            audio_chunks = split_audio(adjusted_audio, temp_folder, start_index)
            transcriptions = transcribe_audio(audio_chunks, parallel, language_code)
            for chunk_path, _ in audio_chunks:
                if os.path.exists(chunk_path):
                    safe_move(chunk_path, os.path.join(audio_folder, os.path.basename(chunk_path)))
            existing_labels.update(transcriptions)
            with open(labels_file, "w") as f:
                json.dump(existing_labels, f, indent=4)
            rename_and_update_labels(dataset_folder)
            csv_labels(existing_labels, dataset_folder)
            logging.info(f"Dataset updated successfully in '{dataset_folder}'.")

        finally:
            shutil.rmtree(temp_folder)
            logging.info(f"Temporary folder {temp_folder} removed.")
    
    elif dataset_type == "2":
        dataset_name = "Separated_Dataset"
        dataset_folder = input("Enter existing dataset folder path: ").strip() 
        dataset_output_folder = input("Enter output folder path(or Leave Empty to save in Current Directory): ").strip() or "Saperated_Dataset"
        algorithm = input("Choose algorithm\n1. K-Fold\n2. Random Split\n3. Stratified Split\n4. Stratified K-Fold\n>>> ").strip()
        if algorithm == "1":
            folds = int(input("Enter number of folds(Or Leave Empty for Default 10-Fold): ").strip() or "10")
            algo.k_fold(dataset_folder,dataset_output_folder,folds)
                       
        elif algorithm != "1" & algorithm <= "4":
            print("Funtions Under Development Please Wait for Future Updates\nSupport SugarCube to get the fuctions faster")
        else :
            print("Invalid choice. Exiting.")
            
    else:
        print("Invalid choice. Exiting.")    