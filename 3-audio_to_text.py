import os
import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('da9Fn8Ke9KDP_d5SKo99VaJ55e6hG-sqHDeJdXN8g1OP')
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url('https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/51769b15-84b3-4ead-b824-5cf4cdd69495')

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        FileName=r'E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\aResult\\'+ofiles[i][-12:-4]+"-.txt"
        raw = open(FileName, "w+")
        print(json.dumps(data, indent=2),file=raw)
        raw.close()

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

myRecognizeCallback = MyRecognizeCallback()

path=r"E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\aResult"
ofiles=os.listdir(path)
ofiles=[path+"\\"+f for f in ofiles if f.endswith('.wav')]
for i in range(len(ofiles)):
    ###
    print(ofiles[i])
    with open(join(dirname(__file__), r'E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\aResult\\',
                   ofiles[i]),'rb') as audio_file:
        audio_source = AudioSource(audio_file)
        speech_to_text.recognize_using_websocket(
            audio=audio_source,
            content_type='audio/wav',
            recognize_callback=myRecognizeCallback,
            model='zh-CN_BroadbandModel',
            #keywords=['colorado', 'tornado', 'tornadoes'],
            #keywords_threshold=0.5,
            max_alternatives=0)

##apikey:da9Fn8Ke9KDP_d5SKo99VaJ55e6hG-sqHDeJdXN8g1OP
##url:https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/51769b15-84b3-4ead-b824-5cf4cdd69495
#path:E:\originD\2019-2020\2019-2020-2\信存检\作业\小组作业\atotlist
#language:zh-CN_BroadbandModel