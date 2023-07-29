import os
import speech_recognition as sr
from pydub import AudioSegment
import yt_dlp as youtube_dl

def download_video(url, channel_name, video_title):
    filename = f"{channel_name}/{video_title}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': filename + '.%(ext)s',  # This will add the correct extension to the file
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename + '.wav'  # We know the file is a .wav file because we specified that in 'preferredcodec'



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

def transcribe_youtube_videos(urls, channel_name, check_existing=True):
    os.makedirs(channel_name, exist_ok=True)
    for i, url in enumerate(urls):
        print(f"Downloading video {i+1}/{len(urls)}...")
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None).replace("/", "_")  # Avoid potential issues with slashes in filenames
        filename = download_video(url, channel_name, video_title)
        print("Download complete. Transcribing...")
        output_file = f"{channel_name}/{video_title}.txt"
        if check_existing and os.path.isfile(output_file):  # Skip transcription if it already exists
            print(f"Transcription for video {video_title} already exists. Skipping.")
            continue
        transcribe_video(filename, output_file)
        os.remove(filename)  # Remove the video file after transcription

def fetch_most_viewed(channel_id):
    # Import YouTube Data API
    from googleapiclient.discovery import build
    # Set up the API
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "YOUR_API_KEY"  # Replace with your API key
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    # Perform the search
    search_response = youtube.search().list(
        channelId=channel_id,
        order="viewCount",
        type="video",
        maxResults=50,  
        part="id",
    ).execute()
    # Extract video URLs
    urls = []
    for search_result in search_response.get("items", []):
        urls.append("https://www.youtube.com/watch?v=" + search_result["id"]["videoId"])
    return urls

def main():
    choice = input("Choose an option:\n1. Provide video links manually\n2. Transcribe all videos from a YouTube channel\n3. Specify the number of most popular videos to transcribe\n4. Fetch the top 50 most viewed videos from a YouTube channel (faster option)\n")

    if choice == "1":
        num_links = int(input("Enter the number of video links: "))
        urls = []
        for i in range(num_links):
            url = input(f"Enter video link {i+1}: ")
            urls.append(url)
        channel_name = input("Enter a name for the manual channel: ")
        transcribe_youtube_videos(urls, channel_name, check_existing=False)
    elif choice == "2":
        channel_url = input("Enter the YouTube channel URL: ")
        with youtube_dl.YoutubeDL() as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)
            channel_name = channel_info['title'].replace("/", "_")  # Avoid potential issues with slashes in directory names
            urls = [video['webpage_url'] for video in channel_info['entries']]
        transcribe_youtube_videos(urls, channel_name)
    elif choice == "3":
        channel_url = input("Enter the YouTube channel URL: ")
        num_videos = int(input("Enter the number of most popular videos to transcribe: "))
        with youtube_dl.YoutubeDL() as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)
            channel_name = channel_info['title'].replace("/", "_")  # Avoid potential issues with slashes in directory names
            all_videos = sorted(channel_info['entries'], key=lambda x: x['view_count'], reverse=True)
            urls = [video['webpage_url'] for video in all_videos[:num_videos]]
        transcribe_youtube_videos(urls, channel_name)
    elif choice == "4":
        channel_url = input("Enter the YouTube channel URL: ")
        with youtube_dl.YoutubeDL() as ydl:
            channel_info = ydl.extract_info(channel_url, download=False)
            channel_name = channel_info['title'].replace("/", "_")  
            urls = fetch_most_viewed(channel_info['id'])  # New function to fetch most viewed videos
        transcribe_youtube_videos(urls, channel_name)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
