# Speech_Dialog_System_using_ChatGPT

## 概要
`Speech_Dialog_System_using_ChatGPT` は、Chat GPTを使用した音声対話アプリです。このアプリケーションは、ユーザーの声の問いかけに対して自動で応答することができます。初めに、Voice Voxを使って「何かご用ですか？」と尋ね、その後、ユーザーの音声入力を受け付けます。

## 機能
- **音声出力**: Voice Voxを通じて「何かご用ですか？」という問いをユーザーに対して自動的に行います。
- **音声入力受付**: ユーザーからの音声入力を受け付けます。
- **音声テキスト化**: Speech Recognitionを使用して、受け取った音声をテキストデータに変換します。
- **応答生成**: テキスト化したデータをChatGPTのAPIに送信し、生成された応答を取得します。
- **応答読み上げ**: ChatGPTからの返信を再びVoice Voxを使用して音声としてユーザーに読み上げます。

## 技術スタック
- Voice Vox
- Speech Recognition
- ChatGPT API
