import requests
import simpleaudio as sa
import speech_recognition as sr
import openai

# OpenAI APIキーの設定
openai.api_key = "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"

# No1
# テキストデータを用意
text = "何かご用ですか？"

# テキストをVOICEVOX ENGINEに送信して音声合成クエリを生成
response = requests.post(
    "http://127.0.0.1:50021/audio_query?speaker=1", params={"text": text}
)
response.raise_for_status()  # エラーがあれば例外を発生させる
query = response.json()  # クエリデータを取得

# クエリデータを使って音声合成を実行
response = requests.post(
    "http://127.0.0.1:50021/synthesis?speaker=1",
    json=query,
    headers={"Content-Type": "application/json"},
)
response.raise_for_status()  # エラーがあれば例外を発生させる

# 音声データをファイルに保存
with open("audio.wav", "wb") as f:
    f.write(response.content)

print("音声ファイルが生成されました。ファイル名: audio.wav")


# 音声ファイルをロード
wave_obj = sa.WaveObject.from_wave_file("audio.wav")

# 再生
play_obj = wave_obj.play()

# 再生が終了するまで待つ
play_obj.wait_done()

# No2
# 音声認識オブジェクトの初期化
recognizer = sr.Recognizer()

# マイクの設定
with sr.Microphone() as source:
    print("Say something!")

    # マイクからの音声を取得
    audio_data = recognizer.listen(source)

    try:
        # Googleの音声認識APIを使用して音声をテキストに変換
        text = recognizer.recognize_google(audio_data)
        print("Google Speech Recognition thinks you said " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )

# No3
# OpenAIのChatGPTにテキストデータを送信し返答を取得
response = openai.chat.completions.create(
    model="gpt-3.5-turbo", messages=text  # 使用するモデル
)
print("ChatGPT's response:", response.choices[0].text.strip())
