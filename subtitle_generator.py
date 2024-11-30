import os
from moviepy import VideoFileClip
import speech_recognition as sr
from tqdm import tqdm

def extract_audio_from_video(video_path, audio_path):
    """
    Extract audio from the video file and save as a .wav file.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted to: {audio_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
    return audio_path

def generate_subtitles_from_audio(audio_path, language='en-US'):
    """
    Generate subtitles from audio using speech recognition.
    """
    recognizer = sr.Recognizer()
    subtitles = []
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            print("Recognizing speech...")

            # Use Google Web Speech API to recognize speech
            text = recognizer.recognize_google(audio, language=language)

            # Split text into subtitle segments
            segment_length = 10  # Approximate seconds
            words = text.split()
            segments = [words[i:i + 20] for i in range(0, len(words), 20)]  # 20 words per segment

            # Create subtitle segments with timestamps
            start_time = 0
            for i, segment in tqdm(enumerate(segments), total=len(segments), desc="Generating Subtitles"):
                end_time = start_time + segment_length
                subtitle = f"{i + 1}\n{format_time(start_time)} --> {format_time(end_time)}\n{' '.join(segment)}\n\n"
                subtitles.append(subtitle)
                start_time = end_time

            print("Subtitles generated.")
    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return None
    return subtitles

def format_time(seconds):
    """
    Format seconds to HH:MM:SS,MS for subtitle timing.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def save_subtitles_to_file(subtitles, output_file):
    """
    Save generated subtitles to an .srt file.
    """
    try:
        with open(output_file, "w") as file:
            file.writelines(subtitles)
        print(f"Subtitles saved to: {output_file}")
    except Exception as e:
        print(f"Error saving subtitles: {e}")

def generate_subtitles(video_path, subtitle_file, language='en-US'):
    """
    Full process to extract audio, recognize speech, and generate subtitles.
    """
    # Step 1: Extract audio from video
    audio_path = "temp_audio.wav"
    audio_file = extract_audio_from_video(video_path, audio_path)
    if not audio_file:
        return

    # Step 2: Generate subtitles from audio
    subtitles = generate_subtitles_from_audio(audio_file, language=language)
    if not subtitles:
        return

    # Step 3: Save subtitles to a .srt file
    save_subtitles_to_file(subtitles, subtitle_file)

    # Clean up the temporary audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ").strip()
    subtitle_file = input("Enter the output subtitle file path (e.g., subtitles.srt): ").strip()
    language = input("Enter the language code (default 'en-US'): ").strip() or 'en-US'

    if not os.path.exists(video_path):
        print(f"Error: The video file {video_path} does not exist.")
    else:
        generate_subtitles(video_path, subtitle_file, language=language)
