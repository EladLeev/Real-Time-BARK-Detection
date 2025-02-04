# Real Time Dog Bark Detection

A fork of [robertanto/Real-Time-Sound-Event-Detection](https://github.com/robertanto/Real-Time-Sound-Event-Detection), modified to detect Dog barks, plus some extra fancy features like:

* Get a Telegram notifications when a bark is detected.
* Cool-down period between barks to avoid channel spam.
* Local log of the detected barks.
* An option to play a calm down sounds, when bark is detected.

This project was forked and modified to deal with dog separation anxiety, and should use caution. **This is not a replacement for a certified dog trainer**.

## Usage

Start by creating your own [Telegram bot](https://www.directual.com/lesson-library/how-to-create-a-telegram-bot).  
Once the channel is ready, to use the tool simply set up the `TELEGRAM_TOKEN` and `CHAT_ID` environment variables, or preferably use `.env` file.  
To play an audio clip when bark is detected, use the `AUDIO_FILE_PATH` to set the file location, and set `PLAY_AUDIO` to `true`.

### Use in venv

Create a virtual environment with all the dependencies using:

```bash
python -m venv venv
pip install -r requirements.txt
```

Run the tool:

```bash
TELEGRAM_TOKEN=<TOKEN>
CHAT_ID=<CHAT_ID>
AUDIO_FILE_PATH=<PATH>
PLAY_AUDIO=true

python3 ./sound_event_detection.py
```

## Privacy & Legal Considerations

### Audio Recording Notices

* This tool continuously records audio from your microphone to detect dog barks.
* Audio is processed locally and in real-time - no audio data is stored or transmitted except for timestamps of detected barks.
* Be mindful of your jurisdiction's laws regarding audio recording, especially if using this in shared spaces or where others may be recorded.

### Responsible Use

* This tool is intended for monitoring your own dogs with their wellbeing in mind.
* Do not use this tool to record conversations or for surveillance purposes.
* Inform household members and visitors that audio monitoring is in use.
* Consider posting notices if used in shared spaces.

### Data Collection

* Only bark detection timestamps are logged locally
* Telegram notifications contain only detection time and event type
* No audio samples are saved or transmitted
