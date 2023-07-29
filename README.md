# YTtransciberPro
Streamline YouTube video transcription with a powerful tool. Utilizes YouTube Data API, yt_dlp, pydub, &amp; speech_recognition for accurate transcriptions. Effortlessly download videos and obtain transcripts. Free, simple, and efficient!

## Key Features

- Transcribe YouTube videos from channels or custom video links.
- Option to transcribe most popular videos for optimized usage.
- Generate individual or consolidated transcriptions.
- Automatic audio extraction and conversion.
- User-friendly command-line interface.
- Practical, Easy, Free.

## Getting Started

1. Clone the repository: `git clone https://github.com/yourusername/YTtransciberPro.git`
2. Install required dependencies: `pip install -r requirements.txt`
3. Run the script: `python main.py`

## Usage

1. Choose a transcription option from the menu.
2. Follow the prompts to input YouTube channel URL or video links.
3. Obtain transcriptions in seconds!

## Details of Options

1. **Provide video links manually:** You can manually enter YouTube video URLs that you want to transcribe.
2. **Transcribe videos from a YouTube channel:** This will download and transcribe all videos from the inputted YouTube channel.
3. **Specify the number of most popular videos to transcribe:** This option allows you to transcribe a specific number of the most viewed videos from a YouTube channel.
4. **Fetch the top 50 most viewed videos from a YouTube channel:** This option utilizes the YouTube Data API to fetch the top 50 most viewed videos from a YouTube channel and transcribes them. The key reasons for this option are:

   - **Improved Efficiency:** Instead of fetching all video links and then sorting by view count, we fetch only the top 50 most viewed videos directly. This reduces the data fetching and processing time significantly.
   - **Resource Optimization:** The application needs to make fewer calls to the YouTube Data API and download fewer video details, reducing the resource usage.
   - **Faster Results:** As fewer videos are processed, transcriptions can be delivered more quickly. Note, however, that due to the limitations of the YouTube Data API, it does not guarantee that the fetched videos are the absolute most viewed videos from the channel.




## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines.

## Issues

If you encounter any bugs or have suggestions, please [open an issue](https://github.com/yourusername/YTtransciberPro/issues).

Enjoy effortless YouTube video transcriptions with YTtransciberPro!
