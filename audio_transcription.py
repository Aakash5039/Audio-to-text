import streamlit as st
import assemblyai as aai
from tempfile import NamedTemporaryFile
from datetime import timedelta

# Set AssemblyAI API key
aai.settings.api_key = "8c0878d067844c3dbac8cc879a12d5a9"

# Function to transcribe audio and generate diarized transcription with timestamps
def transcribe_and_diarize(audio_file):
    try:
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcript = aai.Transcriber().transcribe(audio_file.name, config)
        return transcript
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

# Function to perform Q&A
def question_answer(transcript, question):
    try:
        result = transcript.lemur.task(question)
        return result.response
    except Exception as e:
        st.error(f"Error in Q&A: {e}")
        return None

def format_timestamp(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def main():
    st.title("Talk2Text: Converting Your Voice into Words")

    # Allow user to upload an audio file
    uploaded_file = st.file_uploader("Please upload your audio file here", type=["mp3", "wav"])

    if uploaded_file:
        # Temporary file to store uploaded audio
        with NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio.seek(0)  # Move to the start of the file for reading

        # Transcribe audio and generate diarized transcription with timestamps
        transcript = transcribe_and_diarize(temp_audio)

        if transcript:
            # Display diarized transcription with timestamps
            st.subheader("The Transcription of Audio file...")
            current_speaker = ""

            for utterance in transcript.utterances:
                # Check if speaker has changed
                if utterance.speaker != current_speaker:
                    current_speaker = utterance.speaker
                    st.write(f"Speaker {current_speaker}:")

                # Calculate timestamp
                timestamp = format_timestamp(utterance.start)
                st.write(f"[{timestamp}]: {utterance.text}")

            # Option for Q&A
            # if st.checkbox("Perform Question & Answer"):
            #     question = st.text_input("Enter your question")
            #     if st.button("Ask"):
            #         answer = question_answer(transcript, question)
            #         if answer:
            #             st.subheader("Answer:")
            #             st.write(answer)
            #         else:
            #             st.error("Error occurred during Q&A")

if __name__ == "__main__":
    main()
