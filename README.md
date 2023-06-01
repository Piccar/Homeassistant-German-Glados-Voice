#  Homeassistant-German-Glados-Voice


This project enables you to replace the MaryTTS text-to-speech application in Home Assistant with a German GLaDOS-like voice. It utilizes the gtts library for text-to-speech and performs pitch correction to achieve the desired voice effect.
## Prerequisites

    Python 3.x
    gtts library: Install using pip install gTTS
    Other required dependencies: numpy, matplotlib, soundfile, scipy, pydub, librosa, psola
    Home Assistant: Make sure you have Home Assistant installed and running

## Installation

    Clone or download the project files from the repository.

    Install the required Python dependencies using the following command:

    

    pip install gtts numpy matplotlib soundfile scipy pydub librosa

## Set up the Home Assistant integration:

    Locate the configuration.yaml file in your Home Assistant installation directory.

    Open the file in a text editor and find the tts section.

    Add the following configuration to specify the new GLaDOS voice:

    tts:
     - platform: marytts
       host: IP-Of-Server
       port: 59125
       codec: "WAVE_FILE"

        Replace IP-Of-Server with the Ip of the Server this Python Script is running.

        Save the changes and restart Home Assistant to apply the configuration.

## Configuration Options

The app.py file provides some configurable options:

    frame_length_input: The frame length used for pitch estimation (default: 2048)
    fmin_input and fmax_input: The minimum and maximum frequencies considered during pitch estimation (default: C2 and C7, respectively)
    pitch: The desired pitch correction value (default: 8, adjust as needed for the GLaDOS-like effect)

Feel free to modify these options to achieve your desired voice characteristics.

## License

This project is licensed under the MIT License.
## Acknowledgments

The project utilizes the gtts library for text-to-speech, which is built on the Google Translate text-to-speech service.
Pitch correction is performed using the librosa and psola libraries.
Thanks to [Germancoding](https://github.com/GermanCoding) for fixing the Flask bug and [janprzy](https://github.com/janprzy) for helping to install the dependencies on Linux.
Also a big thanks to [Jan Wilczek](https://github.com/JanWilczek) where I got the idea how to get the autotune effect. You should read the [blog entry or watch the video](https://thewolfsound.com/how-to-auto-tune-your-voice-with-python/).

## Disclaimer    
Disclaimer: This project is not affiliated, endorsed, or sponsored by Valve Corporation. The character GLaDOS mentioned here is a fictional character from the video game "Portal," developed and owned by Valve Corporation. Any references made to GLaDOS are purely for illustrative and entertainment purposes. The use of GLaDOS' voice or any related materials is not intended to infringe upon Valve Corporation's intellectual property rights. This project is created by Piccar and is an independent endeavor.



 If anyone is wondering why i had to convert the mp3 to a wav. Linux was not happy. It could run on windows without conversion... 
