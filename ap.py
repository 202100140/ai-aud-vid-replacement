'''import os
import requests
from moviepy.editor import VideoFileClip
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech
import streamlit as st

# Set the environment variable for Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/speech-to-text-demo-438919-dd23330d4f23.json"


# Function to extract audio from the video
def extract_audio(video_path):
    video_clip = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video_clip.audio.write_audiofile(audio_path)
    return audio_path


# Function to transcribe audio using Google Speech-to-Text
def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    response = client.recognize(config=config, audio=audio)
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription


# Function to correct the transcription using GPT-4o via Azure
def correct_transcription(transcription, api_key, endpoint_url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [{"role": "user", "content": f"Correct the following transcription: {transcription}"}],
        "max_tokens": 500
    }
    response = requests.post(endpoint_url, headers=headers, json=data)

    if response.status_code == 200:
        corrected_text = response.json()["choices"][0]["message"]["content"]
        return corrected_text
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# Azure OpenAI API Key and Endpoint
api_key = "22ec84421ec24230a3638d1b51e3a7dc"
endpoint_url = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"


# Function to generate audio using Google Text-to-Speech
def generate_speech(corrected_text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=corrected_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-J"  # Replace with the desired voice name
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    output_path = "corrected_audio.mp3"
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    return output_path


# Function to replace audio in the original video
def replace_audio(video_path, new_audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(new_audio_path)
    final_video = video_clip.set_audio(audio_clip)
    output_path = "final_video_with_corrected_audio.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path


# Streamlit application
st.title("Video Audio Replacement with AI-Generated Voice")
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if video_file:
    video_path = video_file.name
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    st.write("Extracting audio...")
    audio_path = extract_audio(video_path)

    st.write("Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    st.write("Transcription:", transcription)

    st.write("Correcting transcription...")
    corrected_text = correct_transcription(transcription, api_key, endpoint_url)
    st.write("Corrected Transcription:", corrected_text)

    st.write("Generating corrected audio...")
    corrected_audio_path = generate_speech(corrected_text)

    st.write("Replacing audio in video...")
    final_video_path = replace_audio(video_path, corrected_audio_path)

    st.write("Processing complete! Here is your video with corrected audio:")
    st.video(final_video_path)
    st.write("Download the corrected video:")
    st.download_button("Download Video", open(final_video_path, "rb"), "corrected_video.mp4")'''
import os
import requests
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import speech_v1 as speech
from google.cloud import texttospeech

# Set the environment variable for Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/speech-to-text-demo-438919-dd23330d4f23.json"  # Update this path as needed

def main():
    st.title("AI-Powered Video Audio Replacement Tool")

    # Azure OpenAI connection details
    azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc"  # Provided API Key
    azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  # Provided Endpoint URL

    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    if video_file:
        video_path = video_file.name
        with open(video_path, "wb") as f:
            f.write(video_file.read())

        st.write("Extracting audio...")
        audio_path = extract_audio(video_path)

        st.write("Transcribing audio...")
        transcription = transcribe_audio(audio_path)
        st.write("Transcription:", transcription)

        st.write("Correcting transcription...")
        corrected_text = correct_transcription(transcription, azure_openai_key, azure_openai_endpoint)
        st.write("Corrected Transcription:", corrected_text)

        if corrected_text:
            st.write("Generating corrected audio...")
            corrected_audio_path = generate_speech(corrected_text)

            st.write("Replacing audio in video...")
            final_video_path = replace_audio(video_path, corrected_audio_path)

            st.write("Processing complete! Here is your video with corrected audio:")
            st.video(final_video_path)
            st.write("Download the corrected video:")
            st.download_button("Download Video", open(final_video_path, "rb"), "corrected_video.mp4")

def extract_audio(video_path):
    video_clip = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video_clip.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    response = client.recognize(config=config, audio=audio)
    transcription = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcription

def correct_transcription(transcription, api_key, endpoint_url):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "messages": [{"role": "user", "content": f"Correct the following transcription: {transcription}"}],
        "max_tokens": 500
    }
    response = requests.post(endpoint_url, headers=headers, json=data)
    if response.status_code == 200:
        corrected_text = response.json()["choices"][0]["message"]["content"]
        return corrected_text
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

def generate_speech(corrected_text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=corrected_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-J"  # Replace with the desired voice name
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    output_path = "corrected_audio.mp3"
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    return output_path

def replace_audio(video_path, new_audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(new_audio_path)
    final_video = video_clip.set_audio(audio_clip)
    output_path = "final_video_with_corrected_audio.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

if __name__ == "__main__":
    main()




