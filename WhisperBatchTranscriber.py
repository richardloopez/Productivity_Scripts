#!/usr/bin/env python3

# Author: Richard Lopez Corbalan
# GitHub: github.com/richardloopez
# Citation: If you use this code, please cite Lopez-Corbalan, R
# Whisper Transcription Script. GitHub repository. "https://github.com/openai/whisper"

################################################# ESSENTIALS  #######################################################

import os
import whisper

# Whisper model to charge. Options: tiny, base, small, medium, large
model = whisper.load_model("large")            ###################################


############################################### OPTION 1: SINGLE FILE TRANSCRIPTION #######################################################

# Transcribe audio file
audio_file = "/home/richard/transcript/S7.m4a"         ##################################
result = model.transcribe(audio_file)

# Save transcription to a text file
output_file = "/home/richard/transcript/S7_transcription.txt"         ########################
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

# Also print the transcription to the console (optional)
print(result["text"])


####################################################### OPTION 2: RECURSIVE TRANSCRIPTION #######################################################

directory = "/home/richard/transcript/audio_files" ###################################

for filename in os.listdir(directory):
    if filename.endswith(".m4a") or filename.endswith(".mp3") or filename.endswith(".wav"):  # Add more audio formats if needed
        audio_path = os.path.join(directory, filename)
        result = model.transcribe(audio_path)
        
        # Save transcription to a text file with the same name as the audio file
        output_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}_transcription.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        # Print the transcription to the console (optional)
        print(f"Transcription for {filename}:\n{result['text']}\n")
        
