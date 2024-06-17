import logging
import os

import requests
import simpleaudio as sa
import speech_recognition as sr
from openai import OpenAI

# OpenAI APIキーの設定
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ログの基本設定
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# main.py <-> Voice Vox
class VoiceSynthesizer:
    def __init__(self, base_url, speaker_id=1):
        self.base_url = base_url
        self.speaker_id = speaker_id

    def synthesize_text_to_audio(self, text):
        query = self._get_synthesis_query(text)
        return self._synthesize_audio(query)

    def _get_synthesis_query(self, text):
        response = requests.post(
            f"{self.base_url}/audio_query?speaker={self.speaker_id}",
            params={"text": text},
        )
        response.raise_for_status()
        return response.json()

    def _synthesize_audio(self, query):
        response = requests.post(
            f"{self.base_url}/synthesis?speaker={self.speaker_id}",
            json=query,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.content

    def save_audio_to_file(self, audio_content, filename):
        with open(filename, "wb") as f:
            f.write(audio_content)
        print(f"音声ファイルが生成されました。ファイル名: {filename}")


class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.wave_obj = sa.WaveObject.from_wave_file(filename)

    def play_audio(self):
        play_obj = self.wave_obj.play()
        play_obj.wait_done()


base_url = "http://127.0.0.1:50021"
opening_text = "何かご用ですか？"
filename = "audio.wav"

synthesizer = VoiceSynthesizer(base_url)
audio_content = synthesizer.synthesize_text_to_audio(opening_text)
synthesizer.save_audio_to_file(audio_content, filename)

player = AudioPlayer(filename)
player.play_audio()


# mian.py <-> Speech Recognition
class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech_from_mic(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio_data = self.recognizer.listen(source, timeout=5)
            try:
                text = self.recognizer.recognize_google(audio_data, language="ja-JP")
                print(text)
                logging.info("Google Speech Recognition thinks you said: " + text)
                return text
            except sr.UnknownValueError:
                logging.error("Google 3Speech Recognition could not understand audio")
                return None
            except sr.RequestError as e:
                logging.error(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )
                return None


# main.py <-> ChatGPT
class ChatGPT:
    def __init__(self, api_key):
        self.model = "gpt-3.5-turbo"
        self.session_history = []  # 会話履歴を保持するリスト

    def get_response(self, text):
        if text:
            # 会話履歴を更新
            self.session_history.append({"role": "user", "content": text})
            response = client.chat.completions.create(
                model=self.model, messages=self.session_history
            )
            # レスポンスを履歴に追加
            self.session_history.append(
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content.strip(),
                }
            )
            return response.choices[0].message.content.strip()
        else:
            logging.error("No input to respond to")
            return "No input to respond to."


if __name__ == "__main__":
    speech_to_text = SpeechToText()
    chat_gpt = ChatGPT(api_key="your_openai_api_key")

    try:
        while True:  # 無限ループでユーザー入力を続ける
            text = speech_to_text.recognize_speech_from_mic()
            if text is None:
                print("No speech detected, try again...")
                continue  # 音声が検出されなかった場合はスキップ
            response = chat_gpt.get_response(text)
            print("ChatGPT's response:", response)

            # ChatGPTの応答を音声に変換して再生
            synthesizer = VoiceSynthesizer(base_url)
            response_audio_content = synthesizer.synthesize_text_to_audio(response)
            response_filename = "response_audio.wav"
            synthesizer.save_audio_to_file(response_audio_content, response_filename)
            player = AudioPlayer(response_filename)
            player.play_audio()

    except KeyboardInterrupt:
        print("Exiting the program...")
