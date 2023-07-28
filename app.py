import os
from pathlib import Path
import streamlit as st
from pytube import YouTube
import openai
from zipfile import ZipFile
import whisper
import json

# Load OpenAI API key from config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)

KEY = config_data['openai_api_key']
openai.api_key = KEY


# Load the pre-trained model (cached to avoid repeated loading)
@st.cache_resource
def load_model():
    """Load the pre-trained Whisper ASR model."""
    model = whisper.load_model("base")
    return model

# Function to save audio from YouTube video
@st.cache_resource
def save_audio(url):
    """Download audio from the given YouTube video URL.

    Parameters:
        url (str): The YouTube video URL.

    Returns:
        tuple: A tuple containing the video title and the downloaded audio file name.
    """
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, _ = os.path.splitext(out_file)
    file_name = f"{base}.mp3"
    try:
        os.rename(out_file, file_name)
    except:
        os.remove(file_name)
        os.rename(out_file, file_name)

    audio_file_name = Path(file_name).stem + ".mp3"
    print(f"{yt.title} Successfully downloaded")  # Print success message
    print(file_name)  # Print the audio file name
    print(audio_file_name)  # Print the processed audio file name
    return yt.title, audio_file_name

# Get Transcript from audio file
@st.cache_resource
def audio_to_transcript(audio_file):
    """Transcribe the given audio file using the Whisper ASR model.

    Parameters:
        audio_file (str): The path to the audio file.

    Returns:
        str: The transcribed text.
    """
    model = load_model()  # Load the cached model
    result = model.transcribe(audio_file)  # Transcribe audio using the loaded model
    transcript = result['text']
    return transcript

# Convert transcript to news article using OpenAI's GPT-3 model

def text_new_article(text, word_limit):
    """Generate a news article from the given text using OpenAI's GPT-3 model.

    Parameters:
        text (str): The input text to base the article on.

    Returns:
        str: The generated news article text.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Write a news article in {word_limit} words from the below text:\n" + text,
        temperature=0.7,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text']

def main():
    """Main function to run the News Article Generator app."""
    #Logo
    # st.image('./imgs/logo.jpg', width=100)
    st.set_page_config(
    page_title="YouTube Video to Blog Post",
    page_icon="🧊",
    initial_sidebar_state="expanded"
    )
    st.markdown("##  **YouTube Video To Blog Article Generator**📝\n\n")
    st.write("A ChatGPT power application that helps to generate high quality blog post from a youtube video. ")
    st.write("")

    #option to enter url for youtube video
    url_link = st.text_input("# Enter the video URL here",
                            help="Copy the link of youtube video and paste here",
                            placeholder="Enter url here")


    #Layout
    col1, col2 = st.columns(2)
    #option to set world limit for the article
    with col1:
        word_limit = st.number_input("Set Word count limit (max: 1500)", min_value=100, max_value=1500, value=300,
                                help='This will set you world count limit for article.')


    with col2:
    #option to ask user if he/she wants to download result files
        st.write("")
        st.write("")
        ask_download = st.checkbox("Download Output files",
                               help='Check if you want to output files as zip folder')
    if st.button("Start Analysis"):
        with st.spinner("Please Wait..."):
            video_title, audio_file_name = save_audio(url_link)

            st.write("Extrcted Audio file from video:")
            st.audio(audio_file_name)  # Display the downloaded audio
            transcript = audio_to_transcript(audio_file_name)

            st.subheader("Generated Transcript")
            st.success(transcript)  # Display the extracted transcript

            st.subheader("News Article")
            result = text_new_article(transcript, word_limit=word_limit)  # Generate news article from the transcript
        st.success(result)  # Display the generated news article

        if transcript and result and ask_download:
            # Save transcript and article in separate text files
            with open("transcript.txt", 'w') as transcript_text:
                transcript_text.write(transcript)

            with open("article.txt", 'w') as article_text:
                article_text.write(result)

            # Create a zip file containing the transcript and article
            with ZipFile("output.zip", 'w') as zip_file:
                zip_file.write('transcript.txt')
                zip_file.write('article.txt')

            # Provide a download button for the zip file
            with open('output.zip', 'rb') as zip_download:
                btn = st.download_button(
                    label="Download Zip",
                    data=zip_download,
                    file_name="output.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
