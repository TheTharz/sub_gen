import os
import moviepy.editor as mp
import speech_recognition as sr
from tqdm import tqdm

def extract_audio_from_video(video_path, audio_path):
    """
    Extract audio from the video file and save as a .wav file.
    """
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted to: {audio_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
    return audio_path

def generate_subtitles_from_audio(audio_path, language_code="en-US"):
    """
    Generate subtitles from audio using speech recognition.
    """
    recognizer = sr.Recognizer()
    subtitles = []
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            print("Recognizing speech...")

            # Use Google Web Speech API to recognize speech in the specified language
            text = recognizer.recognize_google(audio, language=language_code)

            # Split the text into parts based on some predefined interval (e.g., 10 seconds)
            segment_length = 10  # seconds
            words = text.split()
            segments = [words[i:i + segment_length] for i in range(0, len(words), segment_length)]

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

def generate_subtitles(video_path, subtitle_file, language_code):
    """
    Full process to extract audio, recognize speech, and generate subtitles.
    """
    # Step 1: Extract audio from video
    audio_path = "temp_audio.wav"
    audio_file = extract_audio_from_video(video_path, audio_path)
    if not audio_file:
        return

    # Step 2: Generate subtitles from audio
    subtitles = generate_subtitles_from_audio(audio_file, language_code)
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
    print("Enter the language code for the subtitles (e.g., 'en-US' for English, 'es-ES' for Spanish, 'fr-FR' for French).")
    language_code = input("Language code: ").strip()

    if not os.path.exists(video_path):
        print(f"Error: The video file {video_path} does not exist.")
    else:
        generate_subtitles(video_path, subtitle_file, language_code)
