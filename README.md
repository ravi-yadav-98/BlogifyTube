# BlogifyTube
A ChatGPT Powered App that generates high quality Blog Post from input YuTube Videos
# YouTube Video to Blog Post Generator

## Introduction

The YouTube Video to Blog Post Generator is a powerful application that allows you to create high-quality blog posts from YouTube videos. By leveraging the capabilities of OpenAI's GPT-3 model and Whisper ASR (Automatic Speech Recognition) model, this app streamlines the process of transcribing the audio from a YouTube video and generating a compelling news article based on the transcript.

## Getting Started

To use the app, make sure you have the necessary libraries installed. You can install them using the following command:

```
pip install streamlit pytube openai whisper
```

Additionally, you need to set up your OpenAI API key by placing it in a `config.json` file. The format of the `config.json` file should be as follows:

```json
{
    "openai_api_key": "YOUR_OPENAI_API_KEY"
}
```

## How to Use

1. Launch the app using the following command:

```
streamlit run app.py
```

2. Enter the URL of the YouTube video you want to convert into a blog post in the provided text input field.

3. Choose the desired word count limit for the generated article using the slider.

4. Optionally, you can check the "Download Output files" checkbox to get the output files as a zip folder.

5. Click the "Start Analysis" button to begin the process.

6. The app will download the audio from the YouTube video, transcribe it using the Whisper ASR model, and then generate a news article based on the transcript using OpenAI's GPT-3 model.

7. The extracted audio will be displayed, along with the generated transcript and the final news article.

8. If you opted for the output files download, the app will provide a "Download Zip" button to download the transcript and the news article as a zip file.

## Dependencies

The app relies on the following Python libraries:

- os
- pathlib
- streamlit
- pytube
- openai
- whisper
- json
- zipfile

## Note

Please ensure you have a stable internet connection to access the OpenAI API for generating the news article.

Feel free to contribute to the app's development or suggest improvements!

Happy blogging! 📝🎉