import boto3
import playsound
import speech_recognition as sr
from contextlib import closing

r = sr.Recognizer()
polly = boto3.client("polly")

def voice_to_text():
    with sr.Microphone() as source:
        print("質問は何ですか？")
        audio = r.listen(source)
    return r.recognize_google(audio, language="ja-JP")

def create_text(messages):
    print("考え中...")
    agent = boto3.client(service_name = 'bedrock-agent-runtime')
    #model_arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2'
    model_arn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1'
    kb_id = 'DMT25BCARP'
    query = messages
    response = agent.retrieve_and_generate(
        input = {
            'text': query
        },
        retrieveAndGenerateConfiguration = {
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kb_id,
                'modelArn': model_arn,
            }
        },
    )

    response_text = response['output']['text']
    return response_text

def text_to_voice(text):
    mp3_path = "./speech.mp3"
    response = polly.synthesize_speech(
        Engine='neural',
        Text = text,
        OutputFormat = "mp3",
        VoiceId = "Tomoko"
    )
    audio_stream = response.get("AudioStream")
    if audio_stream :
        with closing(audio_stream) as stream:
            with open(mp3_path, "wb") as file:
                file.write(stream.read())
    playsound.playsound(mp3_path)

while True:
    text = voice_to_text()
    if text == "":
        continue
    print("you:", text)

    response_text = create_text(text)
    print("AI:", response_text)

    text_to_voice(response_text)