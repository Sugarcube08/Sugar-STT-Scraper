import os
import json
import tempfile
import shutil
import logging
import speech_recognition as sr
import ffmpeg
from pydub import AudioSegment, silence
from pydub.effects import low_pass_filter
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # For progress bars



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
    *   Harnessing Excellet technology for Dataset Prepration     *
    *                                                             *
    ***************************************************************

      Let's unlock the power of speech and transform it into text!

    ***************************************************************
    """
    print(banner)


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to extract audio from video
def extract_audio(video_path, output_audio_path):
    output_dir = os.path.dirname(output_audio_path)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Extracting audio from {video_path}...")

    try:
        ffmpeg.input(video_path).output(output_audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000").run(overwrite_output=True)
        logging.info(f"Audio extracted: {output_audio_path}")
    except Exception as e:
        logging.error(f"Error during audio extraction: {e}")

# Function to enhance audio and reduce noise (using pydub low-pass filter)
def enhance_audio(input_path, output_path):
    logging.info(f"Enhancing audio: {input_path}")
    audio = AudioSegment.from_wav(input_path)

    # Apply a low-pass filter to reduce high-frequency noise
    reduced_noise_audio = low_pass_filter(audio, 3000)  # Reduce frequencies above 3000 Hz (adjust as needed)

    reduced_noise_audio.export(output_path, format="wav")
    logging.info(f"Enhanced audio saved: {output_path}")
    return output_path

# Function to adjust speed
def adjust_speed(audio_path, output_path, speed_factor=1.0):
    if speed_factor == 1.0:
        logging.info(f"Speed factor is {speed_factor}, no speed adjustment needed for {audio_path}")
        return audio_path  # No speed change needed

    logging.info(f"Adjusting speed to {speed_factor}x for {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    adjusted_audio = audio.speedup(playback_speed=speed_factor)

    adjusted_audio.export(output_path, format="wav")
    logging.info(f"Speed-adjusted audio saved: {output_path}")
    return output_path

# Function to increase volume (in dB)
def increase_volume(input_path, output_path, gain_db=5):
    logging.info(f"Increasing volume by {gain_db}dB for {input_path}")
    audio = AudioSegment.from_wav(input_path)
    increased_audio = audio + gain_db  # Increase volume by gain_db dB
    increased_audio.export(output_path, format="wav")
    logging.info(f"Volume increased audio saved: {output_path}")
    return output_path

# Function to split audio into chunks (max 5 sec)
def split_audio(audio_path, output_folder, start_index=1, max_duration=5000):
    logging.info(f"Splitting audio: {audio_path}")
    audio = AudioSegment.from_wav(audio_path)
    chunks = silence.split_on_silence(audio, min_silence_len=500, silence_thresh=audio.dBFS - 14)

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

    # Wrap this loop with tqdm to show progress bar
    for i, chunk in enumerate(tqdm(final_chunks, desc="Saving Chunks", unit="chunk"), start=start_index):
        chunk_path = os.path.join(output_folder, f"{i}.ogg")
        chunk.export(chunk_path, format="ogg", codec="libopus")  # OGG for storage
        chunk_paths.append((chunk_path, len(chunk) / 1000))  # Store duration in seconds
        logging.info(f"Saved chunk: {chunk_path}")

    return chunk_paths

# Function to estimate word timestamps
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

# Function to transcribe an individual chunk
def transcribe_chunk(chunk_path, duration):
    recognizer = sr.Recognizer()
    logging.info(f"Transcribing: {chunk_path}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        AudioSegment.from_file(chunk_path).export(temp_wav.name, format="wav")

        with sr.AudioFile(temp_wav.name) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                word_timestamps = estimate_word_timestamps(text, duration)
                logging.info(f"Transcription success: {text}")
            except sr.UnknownValueError:
                word_timestamps = []
                logging.warning("Speech not recognized")
            except sr.RequestError:
                word_timestamps = [{"error": "STT service unreachable"}]
                logging.error("STT service unreachable")

    os.remove(temp_wav.name)  # Delete temporary WAV file

    return chunk_path, word_timestamps

# Function to transcribe audio chunks (sequential or parallel)
def transcribe_audio(chunks, parallel=False):
    labels = {}

    if parallel:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(lambda x: transcribe_chunk(*x), chunks))
    else:
        # Wrap the loop with tqdm to show progress bar during transcription
        results = []
        for chunk in tqdm(chunks, desc="Transcribing Chunks", unit="chunk"):
            result = transcribe_chunk(*chunk)
            results.append(result)

    for chunk_path, word_timestamps in results:
        if word_timestamps:
            labels[os.path.basename(chunk_path)] = word_timestamps
        else:
            os.remove(chunk_path)  # Delete failed chunks
            logging.info(f"Deleted untranscribed chunk: {chunk_path}")

    return labels

# Main function
def main():
    print_banner()
    dataset_type = input("Choose dataset type (1: Training, 2: Testing): ").strip()
    dataset_name = "training" if dataset_type == "1" else "testing"

    dataset_mode = input("Choose mode (1: Create New, 2: Append Existing): ").strip()

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
            return

        labels_file = os.path.join(dataset_folder, "labels.json")
        existing_labels = json.load(open(labels_file)) if os.path.exists(labels_file) else {}

        existing_files = [f for f in os.listdir(audio_folder) if f.endswith(".ogg")]
        start_index = max([int(f.split(".")[0]) for f in existing_files if f.split(".")[0].isdigit()], default=0) + 1
        logging.info(f"Appending to existing dataset at {dataset_folder}")

    else:
        logging.error("Invalid choice. Exiting.")
        return

    input_path = input("Enter the path of video/audio file: ").strip()

    # Default speed factor to 1.0 (normal speed)
    speed_factor = input("Enter speed factor (1.0 = normal, <1.0 = slow, >1.0 = fast): ").strip() or "1.0"
    speed_factor = float(speed_factor)  # Convert to float

    # New option for increasing volume
    increase_volume_choice = input("Do you want to increase the volume beyond original? (y for Yes / n for No): ").strip().lower() or "n"
    gain_db = 0
    if increase_volume_choice == "y":
        gain_db = float(input("Enter gain in dB (e.g., 5 for 5dB increase): ").strip())

    extracted_audio = os.path.join(dataset_folder, "temp.wav")
    if input_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
        extract_audio(input_path, extracted_audio)
    else:
        shutil.copy(input_path, extracted_audio)

    enhanced_audio = enhance_audio(extracted_audio, extracted_audio)

    # Increase volume if required
    if gain_db > 0:
        enhanced_audio = increase_volume(enhanced_audio, extracted_audio, gain_db)

    adjusted_audio = adjust_speed(enhanced_audio, extracted_audio, speed_factor)

    temp_folder = tempfile.mkdtemp()
    audio_chunks = split_audio(adjusted_audio, temp_folder, start_index)

    parallel = input("Use parallel processing? (y for yes /n for no): ").strip().lower() == "y"
    transcriptions = transcribe_audio(audio_chunks, parallel)

    # Move the audio chunks to the final folder
    shutil.move(temp_folder, audio_folder)
    existing_labels.update(transcriptions)
    json.dump(existing_labels, open(labels_file, "w"), indent=4)

    logging.info(f"Dataset updated successfully in '{dataset_folder}'.")

if __name__ == "__main__":
    main()
