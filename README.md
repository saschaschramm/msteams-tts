# Text-to-Speech for Microsoft Teams

This project demonstrates how to integrate OpenAI's Text-to-Speech service with Microsoft Teams using the BlackHole audio loopback driver on MacOS. This allows you to synthesize speech from text directly into your Teams meetings as an audio input.

## Installation

1. **Install BlackHole:**
```bash
brew install blackhole-2ch
```

2. **Install the requirements**
```bash
pip install -r requirements.txt
```

## Configuration
* Open the [Audio MIDI Setup](https://support.apple.com/en-gb/guide/audio-midi-setup/ams59f301fda/mac) application on your Mac. You can search for it using Spotlight.
* Select `BlackHole 2ch` from the list on the left, and then change the format `to 16,000 Hz`.
* Open Microsoft Teams and navigate to the audio settings. Set `BlackHole 2ch` as the microphone device.

## Usage
Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
```bash
export OPENAI_API_KEY=sk-...
```
Run the script:
```bash
python main.py
```
Enter the text you want to synthesize and press `Enter`.
