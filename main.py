import os
import time
from typing import Optional

import pyaudio
from pyaudio import PyAudio
import requests
from requests.models import Response
import wave


# DEVICE_NAME: str = "BlackHole 2ch"
DEVICE_NAME: str = "Studio Display Speakers"
MODEL: str = "tts-1"
VOICE: str = "onyx"


def print_devices(devices: list[str]) -> None:
    print("=== Available devices")
    for i, device in enumerate(devices):
        print(f"{i}: {device}")


def stream(device_index: int, input: str) -> None:
    audio: PyAudio = pyaudio.PyAudio()
    headers: dict[str, str] = {
        "Authorization": f'Bearer {os.getenv("OPENAI_API_KEY")}',
    }

    json: dict[str, str] = {
        "model": MODEL,
        "input": input,
        "voice": VOICE,
        "response_format": "wav",
    }

    response: Response = requests.post(
        url="https://api.openai.com/v1/audio/speech",
        headers=headers,
        json=json,
        stream=True,
    )
    if response.ok:
        with wave.open(f=response.raw, mode="rb") as wave_read:
            stream = audio.open(
                format=audio.get_format_from_width(wave_read.getsampwidth()),
                channels=wave_read.getnchannels(),
                rate=wave_read.getframerate(),  # je kleiner deso langsamer
                output=True,
                output_device_index=device_index,
            )

            while (data := wave_read.readframes(1024)) != b"":
                stream.write(data)

            stream.stop_stream()
            stream.close()
            audio.terminate()


def list_devices() -> list[str]:
    audio = pyaudio.PyAudio()
    devices: list[str] = []
    for device_index in range(audio.get_device_count()):
        devices.append(audio.get_device_info_by_index(device_index)["name"])
    return devices


def find_device_index(name: str) -> Optional[int]:
    devices: list[str] = list_devices()
    for device in devices:
        if name in device:
            return devices.index(device)
    return None


def main() -> None:
    devices: list[str] = list_devices()
    print_devices(devices)
    print("\n=== Selected device")
    if (device_index := find_device_index(DEVICE_NAME)) is None:
        print(f"Device {DEVICE_NAME} not found")
    else:
        print(devices[device_index])
        print("\n")
        while True:
            user_input = input("Input: ")
            stream(device_index, user_input)


if __name__ == "__main__":
    main()
