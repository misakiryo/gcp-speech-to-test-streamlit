import os

from google.cloud import speech

import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GCPからjsonファイル形式で認証情報を引っ張ってくるところ.json'


def transcribe_file(content, lang='日本語'):

    lang_code = {
        '英語にする？': 'en_US',
        'やっぱり日本語かな': 'ja-JP',
        'わんちゃんスペイン語！': 'es-ES'
    }
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED, 
        language_code=lang_code[lang] 
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        st.write(result.alternatives[0].transcript)

st.title('文字起こしアプリだ！')
st.header('概要だよ')
st.write('ここはGoogle Cloud Speech-to-Textを使った文字起こしアプリです。リンクは下だよ。')
st.markdown('<a href="https://cloud.google.com/speech-to-text?hl=ja">Cloud Speech-to-Text</a>',unsafe_allow_html=True)

upload_file = st.file_uploader('ファイルのアップロード', type=['mp3', 'wav'])
if upload_file is not None:
    content = upload_file.read()
    st.subheader('ファイルの詳細だよ')
    file_details = {'FileName': upload_file.name, 'FileType': upload_file.type, 'FileSize': upload_file.size}
    st.write(file_details)
    st.subheader('音声の再生が出来るよ(´ε｀ )')
    st.audio(content)
    st.subheader('言語を決めてね')
    option = st.selectbox('翻訳言語を選択するよ', 
                        ('英語にする？', 'やっぱり日本語かな', 'わんちゃんスペイン語！'))
    st.write('選んでる言語:', option)
    
    st.write('文字起こしするところだよ')
    if st.button('始めるよ！'):
        comment = st.empty()
        comment.write('文字起こしを始めるよ？')
        transcribe_file(content, lang=option)
        comment.write('出来たよ٩(๑´3｀๑)۶')