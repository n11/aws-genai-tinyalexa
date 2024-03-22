# aws-genai-tinyalexa

python3 -m venv .venv
source .venv/bin/activate

brew install portaudio

pip install boto3
pip install playsound
pip install speechrecognition
pip install PyObjC
pip install pyaudio
pip install google-api-python-client
pip install --upgrade setuptools wheel

python3 ./tinyalexa.py

deactivate