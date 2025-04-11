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
        If you liked my Project Consider buying me a coffee ☕

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
    """
    Splits the audio into smaller chunks based on silence and saves them to the output folder.
    """
    try:
        logging.info(f"Splitting audio: {audio_path}")
        audio = AudioSegment.from_wav(audio_path)

        # Ensure the audio file is valid
        if len(audio) == 0:
            raise ValueError("Audio file is empty or invalid.")

        # Split audio based on silence
        chunks = silence.split_on_silence(
            audio,
            min_silence_len=50,  # Minimum silence length in ms
            silence_thresh=audio.dBFS - 16  # Silence threshold
        )

        # Combine smaller chunks to meet max_duration
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

        # Save chunks to the output folder
        os.makedirs(output_folder, exist_ok=True)
        chunk_paths = []

        for i, chunk in enumerate(tqdm(final_chunks, desc="Saving Chunks", unit="chunk"), start=start_index):
            chunk_path = os.path.join(output_folder, f"{i}.ogg")
            chunk.export(chunk_path, format="ogg", codec="libopus")
            chunk_paths.append((chunk_path, len(chunk) / 1000))
            logging.info(f"Saved chunk: {chunk_path}")

        return chunk_paths

    except Exception as e:
        logging.error(f"Error splitting audio: {e}")
        return []

def estimate_word_timestamps(text, duration):
    words = text.split()
    if not words:
        return []

    avg_word_duration = duration / len(words)
    timestamps = []
    start_time = 0.0

    for word in words:
        end_time = start_time + avg_word_duration
        timestamps.append({"word": word, "start": round(start_time, 2), "end": round(end_time, 2)})
        start_time = end_time

    return timestamps

def transcribe_chunk(chunk_path, duration):
    recognizer = sr.Recognizer()
    logging.info(f"Transcribing: {chunk_path}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        AudioSegment.from_file(chunk_path).export(temp_wav.name, format="wav")

        with sr.AudioFile(temp_wav.name) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return chunk_path, text
            except sr.UnknownValueError:
                logging.warning(f"Google Speech Recognition could not understand audio: {chunk_path}")
                return chunk_path, None
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")
                return chunk_path, None
            finally:
                os.remove(temp_wav.name)

def transcribe_audio(chunks, parallel=False):
    labels = {}

    if parallel:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda x: transcribe_chunk(*x), chunks))
    else:
        results = []
        for chunk in tqdm(chunks, desc="Transcribing Chunks", unit="chunk"):
            result = transcribe_chunk(*chunk)
            results.append(result)

    for chunk_path, text in results:
        if text:
            labels[os.path.basename(chunk_path)] = text
        else:
            os.remove(chunk_path)
            logging.info(f"Deleted untranscribed chunk: {chunk_path}")

    return labels

def csv_labels(label_file, dataset_folder):
    labels_csv_path = os.path.join(dataset_folder, "labels.csv")

    print("Creating labels.csv file...")
    data = []
    for chunk, text in label_file.items():
        data.append({
            "Chunk": chunk,
            "Transcription": text
        })

    df = pd.DataFrame(data, columns=["Chunk", "Transcription"])
    df.to_csv(labels_csv_path, index=False)
    print("✅ labels.csv file created successfully!")
