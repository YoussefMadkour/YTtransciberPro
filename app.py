import os
import speech_recognition as sr
from pydub import AudioSegment
import yt_dlp as youtube_dl

def download_video(url, filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': filename,
        'quiet': True,
        'keepvideo': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_video(video_path, output_file):
    audio = AudioSegment.from_wav(video_path)

    r = sr.Recognizer()
    for i in range(0, len(audio), 60000):
        chunk = audio[i:i+60000]
        chunk.export("temp.wav", format="wav")
        with sr.AudioFile('temp.wav') as source:
            audio_listened = r.record(source)
            try:
                print("Transcribing chunk...")
                text = r.recognize_google(audio_listened)
                timestamp = i / 60000
                with open(output_file, 'a') as transcribed_audio_file:
                    transcribed_audio_file.write(f"[{timestamp} minutes]: {text}\n")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except Exception as e:
                print("Could not transcribe audio: ", str(e))
    print("Transcription completed!")
    os.remove("temp.wav")

def transcribe_youtube_videos(urls, single_file=True):
    if single_file:
        output_file = "transcriptions.txt"
    for i, url in enumerate(urls):
        print(f"Downloading video {i+1}/{len(urls)}...")
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        filename = f"{video_title}.wav"
        download_video(url, filename)
        print("Download complete. Transcribing...")
        if not single_file:
            output_file = f"{video_title}.txt"
        transcribe_video(filename, output_file)
        os.remove(filename)  # Remove the video file after transcription

def transcribe_youtube_channel(channel_url, num_videos=None, single_file=True):
    if single_file:
        output_file = "transcriptions.txt"

    ydl_opts = {
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(channel_url, download=False)
        playlist_url = playlist_dict.get('url', None)

        video_urls = []
        if playlist_url:
            ydl.extract_info(playlist_url, download=False)
            for entry in playlist_dict['entries']:
                if entry:
                    video_urls.append(entry['webpage_url'])

    if num_videos is not None:
        if num_videos == 1:
            # Sort videos by view count in descending order and choose the most popular video
            video_urls.sort(key=lambda x: x['view_count'], reverse=True)
            video_urls = video_urls[:1]
        elif num_videos > 1 and num_videos < len(video_urls):
            # Sort videos by view count in descending order and choose the most popular videos based on the number provided
            video_urls.sort(key=lambda x: x['view_count'], reverse=True)
            video_urls = video_urls[:num_videos]

    for i, url in enumerate(video_urls):
        print(f"Downloading video {i+1}/{len(video_urls)}...")
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        filename = f"{video_title}.wav"
        download_video(url, filename)
        print("Download complete. Transcribing...")
        if not single_file:
            output_file = f"{video_title}.txt"
        transcribe_video(filename, output_file)
        os.remove(filename)  # Remove the video file after transcription

def main():
    choice = input("Choose an option:\n1. Transcribe videos from a YouTube channel\n2. Specify the number of most popular videos to transcribe\n3. Specify the number of videos to transcribe and provide video links manually\n")

    if choice == "1":
        channel_url = input("Enter the YouTube channel URL: ")
        transcribe_youtube_channel(channel_url, single_file=False)
    elif choice == "2":
        channel_url = input("Enter the YouTube channel URL: ")
        num_videos = int(input("Enter the number of most popular videos to transcribe: "))
        transcribe_youtube_channel(channel_url, num_videos=num_videos, single_file=False)
    elif choice == "3":
        num_links = int(input("Enter the number of video links: "))
        urls = []
        for i in range(num_links):
            url = input(f"Enter video link {i+1}: ")
            urls.append(url)
        transcribe_youtube_videos(urls, single_file=False)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
